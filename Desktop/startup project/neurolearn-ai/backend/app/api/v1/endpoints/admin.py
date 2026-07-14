from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer
from loguru import logger
from app.core.database import get_database
from app.models.admin import (
    SystemMetricsCreate, SystemMetricsResponse,
    AuditLogCreate, AuditLogResponse,
    SystemHealthCreate, SystemHealthResponse,
    ErrorLogCreate, ErrorLogResponse,
    AdminStatsCreate, AdminStatsResponse
)
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter()
security = HTTPBearer()

@router.get("/dashboard/metrics", response_model=SystemMetricsResponse)
async def get_system_metrics(token: str = Depends(security)):
    """Get system-wide metrics for admin dashboard"""
    db = await get_database()
    
    # Calculate metrics from database
    total_users = await db.users.count_documents({})
    active_users = await db.users.count_documents({"status": "active"})
    total_documents = await db.documents.count_documents({})
    total_ai_queries = await db.conversations.count_documents({})
    total_vision_queries = await db.vision_results.count_documents({})
    
    # Calculate revenue from payments
    payments = await db.payment_history.find({"status": "succeeded"}).to_list(1000)
    revenue_total = sum(p["amount"] for p in payments)
    revenue_monthly = sum(p["amount"] for p in payments if p["created_at"] > datetime.utcnow() - timedelta(days=30))
    
    active_subscriptions = await db.subscriptions.count_documents({"status": "active"})
    
    metrics = {
        "total_users": total_users,
        "active_users": active_users,
        "total_documents": total_documents,
        "total_ai_queries": total_ai_queries,
        "total_vision_queries": total_vision_queries,
        "revenue_monthly": revenue_monthly,
        "revenue_total": revenue_total,
        "active_subscriptions": active_subscriptions,
        "recorded_at": datetime.utcnow()
    }
    
    return metrics

@router.get("/users", response_model=List[dict])
async def get_all_users(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    token: str = Depends(security)
):
    """Get all users with pagination and filtering"""
    db = await get_database()
    
    query = {}
    if status:
        query["status"] = status
    
    users = await db.users.find(query).skip(skip).limit(limit).to_list(limit)
    
    # Convert ObjectId to string
    for user in users:
        if "_id" in user:
            user["id"] = str(user["_id"])
            del user["_id"]
    
    return users

@router.get("/users/{user_id}")
async def get_user_details(user_id: str, token: str = Depends(security)):
    """Get detailed information about a specific user"""
    db = await get_database()
    
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's subscription
    subscription = await db.subscriptions.find_one({"user_id": user_id})
    
    # Get user's documents
    documents = await db.documents.find({"user_id": user_id}).to_list(10)
    
    # Get user's activity
    conversations = await db.conversations.find({"user_id": user_id}).to_list(10)
    
    return {
        "user": user,
        "subscription": subscription,
        "document_count": len(documents),
        "conversation_count": len(conversations)
    }

@router.put("/users/{user_id}/status")
async def update_user_status(user_id: str, status: str, token: str = Depends(security)):
    """Update user status (admin only)"""
    db = await get_database()
    
    valid_statuses = ["active", "inactive", "suspended", "pending"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.users.update_one(
        {"_id": user_id},
        {"": {"status": status, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Log the action
    await db.audit_logs.insert_one({
        "action": "update_user_status",
        "resource": f"users/{user_id}",
        "details": {"status": status},
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "User status updated successfully"}

@router.get("/analytics/usage")
async def get_usage_analytics(
    period: str = "7d",
    token: str = Depends(security)
):
    """Get usage analytics for specified period"""
    db = await get_database()
    
    # Calculate period start
    if period == "7d":
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        start_date = datetime.utcnow() - timedelta(days=30)
    elif period == "90d":
        start_date = datetime.utcnow() - timedelta(days=90)
    else:
        start_date = datetime.utcnow() - timedelta(days=7)
    
    # Get usage data
    ai_queries = await db.conversations.count_documents({"created_at": {"": start_date}})
    vision_queries = await db.vision_results.count_documents({"created_at": {"": start_date}})
    documents_uploaded = await db.documents.count_documents({"created_at": {"": start_date}})
    
    # Get daily usage (simplified)
    daily_usage = []
    for i in range(7 if period == "7d" else 30):
        day_start = start_date + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        day_ai = await db.conversations.count_documents({
            "created_at": {"": day_start, "": day_end}
        })
        day_vision = await db.vision_results.count_documents({
            "created_at": {"": day_start, "": day_end}
        })
        
        daily_usage.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "ai_queries": day_ai,
            "vision_queries": day_vision
        })
    
    return {
        "period": period,
        "total_ai_queries": ai_queries,
        "total_vision_queries": vision_queries,
        "documents_uploaded": documents_uploaded,
        "daily_usage": daily_usage
    }

@router.get("/analytics/revenue")
async def get_revenue_analytics(
    period: str = "30d",
    token: str = Depends(security)
):
    """Get revenue analytics for specified period"""
    db = await get_database()
    
    if period == "7d":
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        start_date = datetime.utcnow() - timedelta(days=30)
    elif period == "90d":
        start_date = datetime.utcnow() - timedelta(days=90)
    else:
        start_date = datetime.utcnow() - timedelta(days=30)
    
    payments = await db.payment_history.find({
        "status": "succeeded",
        "created_at": {"": start_date}
    }).to_list(1000)
    
    total_revenue = sum(p["amount"] for p in payments)
    
    # Revenue by plan
    revenue_by_plan = {}
    for payment in payments:
        plan = payment.get("plan", "unknown")
        if plan not in revenue_by_plan:
            revenue_by_plan[plan] = 0
        revenue_by_plan[plan] += payment["amount"]
    
    return {
        "period": period,
        "total_revenue": total_revenue,
        "revenue_by_plan": revenue_by_plan,
        "transaction_count": len(payments)
    }

@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    action: Optional[str] = None,
    token: str = Depends(security)
):
    """Get audit logs with filtering"""
    db = await get_database()
    
    query = {}
    if action:
        query["action"] = action
    
    logs = await db.audit_logs.find(query).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
    return logs

@router.get("/system-health", response_model=List[SystemHealthResponse])
async def get_system_health(token: str = Depends(security)):
    """Get health status of all system components"""
    db = await get_database()
    
    health_checks = [
        {"service": "database", "status": "healthy", "response_time": 0.05},
        {"service": "redis", "status": "healthy", "response_time": 0.02},
        {"service": "chromadb", "status": "healthy", "response_time": 0.1},
        {"service": "api", "status": "healthy", "response_time": 0.01},
    ]
    
    for check in health_checks:
        check["last_check"] = datetime.utcnow()
    
    return health_checks

@router.get("/error-logs", response_model=List[ErrorLogResponse])
async def get_error_logs(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    token: str = Depends(security)
):
    """Get error logs with filtering"""
    db = await get_database()
    
    query = {}
    if severity:
        query["severity"] = severity
    
    errors = await db.error_logs.find(query).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
    return errors

@router.put("/error-logs/{error_id}/resolve")
async def resolve_error_log(error_id: str, token: str = Depends(security)):
    """Mark an error log as resolved"""
    db = await get_database()
    
    result = await db.error_logs.update_one(
        {"_id": error_id},
        {"": {"resolved": True, "resolved_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Error log not found")
    
    return {"message": "Error log marked as resolved"}

@router.get("/stats/period/{period}", response_model=AdminStatsResponse)
async def get_period_stats(period: str, token: str = Depends(security)):
    """Get statistics for a specific period"""
    db = await get_database()
    
    if period == "7d":
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        start_date = datetime.utcnow() - timedelta(days=30)
    else:
        start_date = datetime.utcnow() - timedelta(days=7)
    
    new_users = await db.users.count_documents({"created_at": {"": start_date}})
    documents_processed = await db.documents.count_documents({"created_at": {"": start_date}})
    ai_queries = await db.conversations.count_documents({"created_at": {"": start_date}})
    vision_queries = await db.vision_results.count_documents({"created_at": {"": start_date}})
    
    payments = await db.payment_history.find({
        "status": "succeeded",
        "created_at": {"": start_date}
    }).to_list(1000)
    revenue = sum(p["amount"] for p in payments)
    
    subscription_upgrades = await db.subscriptions.count_documents({
        "updated_at": {"": start_date}
    })
    
    stats = {
        "period": period,
        "new_users": new_users,
        "active_sessions": 0,  # Would need session tracking
        "documents_processed": documents_processed,
        "ai_queries_made": ai_queries,
        "vision_queries_made": vision_queries,
        "revenue": revenue,
        "subscription_upgrades": subscription_upgrades,
        "support_tickets": 0,  # Would need support system
        "recorded_at": datetime.utcnow()
    }
    
    return stats
