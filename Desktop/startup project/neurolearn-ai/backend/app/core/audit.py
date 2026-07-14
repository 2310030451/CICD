from datetime import datetime
from typing import Optional, Dict, Any
from loguru import logger
from fastapi import Request
from app.core.database import get_database

class AuditLogger:
    """Audit logging system for tracking system events"""
    
    @staticmethod
    async def log_event(
        user_id: Optional[str],
        action: str,
        resource: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success"
    ):
        """Log an audit event to the database"""
        try:
            db = await get_database()
            
            audit_log = {
                "user_id": user_id,
                "action": action,
                "resource": resource,
                "details": details or {},
                "ip_address": ip_address,
                "user_agent": user_agent,
                "status": status,
                "timestamp": datetime.utcnow()
            }
            
            await db.audit_logs.insert_one(audit_log)
            logger.info(f"Audit log: {action} on {resource} by user {user_id}")
        
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
    
    @staticmethod
    async def log_login(user_id: str, ip_address: str, user_agent: str, success: bool = True):
        """Log a login event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="login",
            resource="auth",
            details={"success": success},
            ip_address=ip_address,
            user_agent=user_agent,
            status="success" if success else "failed"
        )
    
    @staticmethod
    async def log_logout(user_id: str, ip_address: str, user_agent: str):
        """Log a logout event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="logout",
            resource="auth",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    @staticmethod
    async def log_document_upload(user_id: str, document_id: str, file_name: str):
        """Log a document upload event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="upload",
            resource=f"documents/{document_id}",
            details={"file_name": file_name}
        )
    
    @staticmethod
    async def log_document_delete(user_id: str, document_id: str, file_name: str):
        """Log a document deletion event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="delete",
            resource=f"documents/{document_id}",
            details={"file_name": file_name}
        )
    
    @staticmethod
    async def log_ai_query(user_id: str, query_type: str, query_length: int):
        """Log an AI query event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="query",
            resource="ai",
            details={
                "query_type": query_type,
                "query_length": query_length
            }
        )
    
    @staticmethod
    async def log_subscription_change(user_id: str, old_plan: str, new_plan: str):
        """Log a subscription change event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="subscription_change",
            resource="subscriptions",
            details={
                "old_plan": old_plan,
                "new_plan": new_plan
            }
        )
    
    @staticmethod
    async def log_permission_denied(user_id: str, action: str, resource: str):
        """Log a permission denied event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="permission_denied",
            resource=resource,
            details={"attempted_action": action},
            status="denied"
        )
    
    @staticmethod
    async def log_rate_limit_exceeded(user_id: str, endpoint: str):
        """Log a rate limit exceeded event"""
        await AuditLogger.log_event(
            user_id=user_id,
            action="rate_limit_exceeded",
            resource=endpoint,
            status="blocked"
        )

class AuditMiddleware:
    """Middleware to automatically log API requests"""
    
    async def __call__(self, request: Request, call_next):
        """Process request and log audit event"""
        # Get request details
        user_id = request.headers.get("X-User-ID")
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("User-Agent")
        
        # Process request
        response = await call_next(request)
        
        # Log the request
        action = request.method.lower()
        resource = request.url.path
        
        # Skip logging for health checks and static files
        if "/health" in resource or "/static" in resource:
            return response
        
        # Determine status based on response status code
        status = "success" if response.status_code < 400 else "error"
        
        await AuditLogger.log_event(
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status
        )
        
        return response

async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    resource: Optional[str] = None,
    limit: int = 100,
    skip: int = 0
):
    """Retrieve audit logs with filtering"""
    try:
        db = await get_database()
        
        query = {}
        if user_id:
            query["user_id"] = user_id
        if action:
            query["action"] = action
        if resource:
            query["resource"] = {"": resource, "": "i"}
        
        logs = await db.audit_logs.find(query).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
        
        return logs
    
    except Exception as e:
        logger.error(f"Failed to retrieve audit logs: {e}")
        return []
