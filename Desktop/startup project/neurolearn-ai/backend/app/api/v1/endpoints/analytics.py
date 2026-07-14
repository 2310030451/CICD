from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.learning_analytics import LearningEventCreate, LearningEvent, Analytics, AnalyticsCreate, AnalyticsPeriod
from app.core.database import get_database
from app.core.auth import decode_token
from loguru import logger


router = APIRouter()


async def get_current_user_id(token: str) -> str:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return payload.get("user_id")


@router.post("/events", response_model=LearningEvent)
async def create_learning_event(
    event: LearningEventCreate,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        event_dict = event.model_dump()
        event_dict["user_id"] = user_id
        event_dict["timestamp"] = datetime.utcnow()
        event_dict["created_at"] = datetime.utcnow()
        
        result = await db.learning_events.insert_one(event_dict)
        event_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Created learning event for user {user_id}")
        return LearningEvent(**event_dict)
    except Exception as e:
        logger.error(f"Failed to create learning event: {e}")
        raise HTTPException(status_code=500, detail="Failed to create learning event")


@router.get("/events", response_model=List[LearningEvent])
async def get_learning_events(
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        events = await db.learning_events.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).skip(offset).limit(limit).to_list(length=limit)
        
        return [LearningEvent(**event) for event in events]
    except Exception as e:
        logger.error(f"Failed to get learning events: {e}")
        raise HTTPException(status_code=500, detail="Failed to get learning events")


@router.post("/analytics", response_model=Analytics)
async def create_analytics(
    analytics: AnalyticsCreate,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        analytics_dict = analytics.model_dump()
        analytics_dict["user_id"] = user_id
        analytics_dict["created_at"] = datetime.utcnow()
        analytics_dict["updated_at"] = datetime.utcnow()
        
        result = await db.analytics.insert_one(analytics_dict)
        analytics_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Created analytics for user {user_id}")
        return Analytics(**analytics_dict)
    except Exception as e:
        logger.error(f"Failed to create analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to create analytics")


@router.get("/analytics", response_model=List[Analytics])
async def get_analytics(
    period: Optional[AnalyticsPeriod] = None,
    limit: int = 10,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        query = {"user_id": user_id}
        if period:
            query["period"] = period
        
        analytics = await db.analytics.find(query).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        return [Analytics(**analytic) for analytic in analytics]
    except Exception as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")
