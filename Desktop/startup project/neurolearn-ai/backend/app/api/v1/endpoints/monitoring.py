from fastapi import APIRouter
from app.core.monitoring import log_system_health, get_system_metrics, cleanup_old_logs, metrics
from loguru import logger

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return await log_system_health()


@router.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return await get_system_metrics()


@router.get("/metrics/summary")
async def get_metrics_summary():
    """Get metrics summary"""
    return metrics.get_all()


@router.post("/cleanup")
async def cleanup_logs(days: int = 30):
    """Clean up old logs"""
    await cleanup_old_logs(days)
    return {"status": "success", "message": f"Cleaned up logs older than {days} days"}
