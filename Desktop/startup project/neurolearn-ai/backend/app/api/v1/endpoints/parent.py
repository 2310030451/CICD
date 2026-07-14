from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from loguru import logger
from app.core.database import get_database
from app.models.parent import (
    ParentChildRelationCreate, ParentChildRelationResponse,
    StudentProgressReportCreate, StudentProgressReportResponse,
    ParentNotificationCreate, ParentNotificationResponse,
    RevisionCalendarCreate, RevisionCalendarResponse
)
from datetime import datetime
from typing import List

router = APIRouter()
security = HTTPBearer()

@router.post("/link-child", response_model=ParentChildRelationResponse)
async def link_child(relation: ParentChildRelationCreate, token: str = Depends(security)):
    """Link a parent to their child"""
    db = await get_database()
    parent_id = token.credentials
    
    relation_data = relation.dict()
    relation_data["parent_id"] = parent_id
    relation_data["created_at"] = datetime.utcnow()
    
    result = await db.parent_child_relations.insert_one(relation_data)
    relation_data["id"] = str(result.inserted_id)
    
    return relation_data

@router.get("/children")
async def get_linked_children(token: str = Depends(security)):
    """Get all children linked to the parent"""
    db = await get_database()
    parent_id = token.credentials
    
    relations = await db.parent_child_relations.find({"parent_id": parent_id}).to_list(50)
    
    child_ids = [r["child_id"] for r in relations]
    children = await db.users.find({"_id": {"": child_ids}}).to_list(50)
    
    return children

@router.get("/child/{child_id}/progress", response_model=StudentProgressReportResponse)
async def get_child_progress(child_id: str, period: str = "monthly", token: str = Depends(security)):
    """Get progress report for a specific child"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to view this child's progress")
    
    # Get child's learning analytics
    analytics = await db.learning_analytics.find({"user_id": child_id}).to_list(10)
    
    # Get child's predictions
    predictions = await db.predictions.find({"user_id": child_id}).sort("created_at", -1).to_list(1)
    
    # Get child's digital twin
    digital_twin = await db.digital_twins.find_one({"user_id": child_id})
    
    # Generate progress report
    report_data = {
        "parent_id": parent_id,
        "child_id": child_id,
        "period": period,
        "exam_predictions": predictions[0] if predictions else {},
        "weak_subjects": digital_twin.get("knowledge_gaps", []) if digital_twin else [],
        "strong_subjects": digital_twin.get("strengths", []) if digital_twin else [],
        "study_hours": sum(a.get("study_time", 0) for a in analytics) if analytics else 0,
        "attendance_percentage": 85.0,  # Would come from attendance records
        "average_score": 75.0,  # Would come from quiz results
        "ai_suggestions": [
            "Focus on weak subjects identified in the digital twin",
            "Increase study hours for better retention",
            "Use spaced repetition for difficult topics"
        ],
        "generated_at": datetime.utcnow()
    }
    
    return report_data

@router.get("/child/{child_id}/predictions")
async def get_child_predictions(child_id: str, token: str = Depends(security)):
    """Get exam predictions for a specific child"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to view this child's predictions")
    
    predictions = await db.predictions.find({"user_id": child_id}).sort("created_at", -1).to_list(5)
    
    return predictions

@router.get("/child/{child_id}/weak-subjects")
async def get_child_weak_subjects(child_id: str, token: str = Depends(security)):
    """Get weak subjects for a specific child"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to view this child's data")
    
    digital_twin = await db.digital_twins.find_one({"user_id": child_id})
    
    if not digital_twin:
        return {"weak_subjects": []}
    
    return {
        "weak_subjects": digital_twin.get("knowledge_gaps", []),
        "recommendations": digital_twin.get("recommendations", [])
    }

@router.get("/child/{child_id}/study-hours")
async def get_child_study_hours(child_id: str, period: str = "week", token: str = Depends(security)):
    """Get study hours for a specific child"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to view this child's data")
    
    # Calculate period start
    if period == "week":
        start_date = datetime.utcnow() - timedelta(days=7)
    elif period == "month":
        start_date = datetime.utcnow() - timedelta(days=30)
    else:
        start_date = datetime.utcnow() - timedelta(days=7)
    
    analytics = await db.learning_analytics.find({
        "user_id": child_id,
        "created_at": {"": start_date}
    }).to_list(100)
    
    total_hours = sum(a.get("study_time", 0) for a in analytics)
    
    return {
        "period": period,
        "total_hours": total_hours,
        "daily_average": total_hours / 7 if period == "week" else total_hours / 30
    }

@router.get("/notifications", response_model=List[ParentNotificationResponse])
async def get_notifications(token: str = Depends(security)):
    """Get notifications for the parent"""
    db = await get_database()
    parent_id = token.credentials
    
    notifications = await db.parent_notifications.find({
        "parent_id": parent_id
    }).sort("created_at", -1).to_list(50)
    
    return notifications

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, token: str = Depends(security)):
    """Mark a notification as read"""
    db = await get_database()
    parent_id = token.credentials
    
    result = await db.parent_notifications.update_one(
        {"id": notification_id, "parent_id": parent_id},
        {"": {"is_read": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}

@router.get("/child/{child_id}/revision-calendar", response_model=List[RevisionCalendarResponse])
async def get_revision_calendar(child_id: str, token: str = Depends(security)):
    """Get revision calendar for a specific child"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to view this child's data")
    
    calendar = await db.revision_calendar.find({
        "child_id": child_id,
        "scheduled_date": {"": datetime.utcnow()}
    }).sort("scheduled_date", 1).to_list(50)
    
    return calendar

@router.post("/child/{child_id}/revision-calendar", response_model=RevisionCalendarResponse)
async def add_revision_item(child_id: str, item: RevisionCalendarCreate, token: str = Depends(security)):
    """Add a revision item to the calendar"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to modify this child's data")
    
    item_data = item.dict()
    item_data["parent_id"] = parent_id
    item_data["child_id"] = child_id
    item_data["created_at"] = datetime.utcnow()
    
    result = await db.revision_calendar.insert_one(item_data)
    item_data["id"] = str(result.inserted_id)
    
    return item_data

@router.get("/child/{child_id}/ai-suggestions")
async def get_ai_suggestions(child_id: str, token: str = Depends(security)):
    """Get AI suggestions for child improvement"""
    db = await get_database()
    parent_id = token.credentials
    
    # Verify parent-child relationship
    relation = await db.parent_child_relations.find_one({
        "parent_id": parent_id,
        "child_id": child_id
    })
    if not relation:
        raise HTTPException(status_code=403, detail="Not authorized to view this child's data")
    
    # Get digital twin for personalized suggestions
    digital_twin = await db.digital_twins.find_one({"user_id": child_id})
    
    # Get recommendations
    recommendations = await db.recommendations.find({"user_id": child_id}).sort("created_at", -1).to_list(1)
    
    suggestions = []
    
    if digital_twin:
        if digital_twin.get("knowledge_gaps"):
            suggestions.append({
                "type": "knowledge_gap",
                "message": f"Focus on improving: {', '.join(digital_twin['knowledge_gaps'][:3])}"
            })
        
        if digital_twin.get("learning_style"):
            suggestions.append({
                "type": "learning_style",
                "message": f"Learning style: {digital_twin['learning_style']}. Adapt study methods accordingly."
            })
    
    if recommendations:
        suggestions.append({
            "type": "recommendation",
            "message": "Check your personalized recommendations for tailored learning paths."
        })
    
    return {
        "suggestions": suggestions,
        "generated_at": datetime.utcnow()
    }
