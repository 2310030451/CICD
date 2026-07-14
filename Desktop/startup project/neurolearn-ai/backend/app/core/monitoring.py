from loguru import logger
from datetime import datetime
from typing import Dict, Any, Optional
from app.core.database import get_database
import asyncio


class MonitoringMetrics:
    """Monitoring metrics collector"""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "api_requests": 0,
            "api_errors": 0,
            "ai_requests": 0,
            "document_uploads": 0,
            "active_users": 0,
            "start_time": datetime.utcnow().isoformat()
        }
    
    def increment(self, metric: str, value: int = 1):
        """Increment a metric"""
        if metric in self.metrics:
            self.metrics[metric] += value
        else:
            self.metrics[metric] = value
    
    def set(self, metric: str, value: Any):
        """Set a metric value"""
        self.metrics[metric] = value
    
    def get(self, metric: str) -> Optional[Any]:
        """Get a metric value"""
        return self.metrics.get(metric)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all metrics"""
        return self.metrics.copy()


metrics = MonitoringMetrics()


async def log_system_health():
    """Log system health metrics"""
    try:
        db = await get_database()
        
        # Check database connection
        await db.command('ping')
        
        # Collect metrics
        health_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics.get_all(),
            "database": "connected",
            "status": "healthy"
        }
        
        logger.info(f"System Health: {health_data}")
        
        # Store in database for historical tracking
        await db.system_health.insert_one(health_data)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}
    
    return {"status": "healthy"}


async def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log error for monitoring"""
    try:
        db = await get_database()
        
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "is_resolved": False
        }
        
        await db.error_logs.insert_one(error_data)
        logger.error(f"Error logged: {error_data}")
        
    except Exception as e:
        logger.error(f"Failed to log error: {e}")


async def get_system_metrics() -> Dict[str, Any]:
    """Get comprehensive system metrics"""
    try:
        db = await get_database()
        
        # Get recent health checks
        recent_health = await db.system_health.find_one(
            sort=[("timestamp", -1)]
        )
        
        # Get error count (last 24 hours)
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        error_count = await db.error_logs.count_documents({
            "timestamp": {"$gte": yesterday.isoformat()}
        })
        
        # Get active users (last hour)
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        active_users = await db.learning_events.distinct(
            "user_id",
            {"timestamp": {"$gte": one_hour_ago.isoformat()}}
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics.get_all(),
            "recent_health": recent_health,
            "error_count_24h": error_count,
            "active_users_1h": len(active_users),
            "status": "healthy"
        }
        
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        return {"status": "error", "error": str(e)}


async def cleanup_old_logs(days: int = 30):
    """Clean up old logs"""
    try:
        db = await get_database()
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Clean up old health logs
        health_result = await db.system_health.delete_many({
            "timestamp": {"$lt": cutoff_date.isoformat()}
        })
        
        # Clean up old error logs (keep unresolved)
        error_result = await db.error_logs.delete_many({
            "timestamp": {"$lt": cutoff_date.isoformat()},
            "is_resolved": True
        })
        
        logger.info(f"Cleaned up {health_result.deleted_count} health logs and {error_result.deleted_count} error logs")
        
    except Exception as e:
        logger.error(f"Failed to cleanup logs: {e}")
