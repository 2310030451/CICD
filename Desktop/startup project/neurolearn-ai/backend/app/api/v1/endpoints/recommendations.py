from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.recommendations import RecommendationCreate, Recommendation
from app.core.database import get_database
from app.core.auth import decode_token
from app.learning.recommendation_engine import recommendation_engine
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


@router.post("/generate", response_model=Recommendation)
async def generate_recommendations(
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        user_data = await db.digital_twins.find_one({"user_id": user_id})
        
        recommendations = await recommendation_engine.generate_recommendations(user_id, user_data or {})
        
        recommendation_dict = {
            "user_id": user_id,
            **recommendations,
        }
        
        result = await db.recommendations.insert_one(recommendation_dict)
        recommendation_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Generated recommendations for user {user_id}")
        return Recommendation(**recommendation_dict)
    except Exception as e:
        logger.error(f"Failed to generate recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


@router.get("/", response_model=List[Recommendation])
async def get_recommendations(
    limit: int = 10,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        recommendations = await db.recommendations.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        return [Recommendation(**rec) for rec in recommendations]
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")
