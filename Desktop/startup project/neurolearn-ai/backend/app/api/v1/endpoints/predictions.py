from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from app.models.predictions import PredictionCreate, Prediction
from app.core.database import get_database
from app.core.auth import decode_token
from app.learning.lstm_model import learning_predictor
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


@router.post("/generate", response_model=Prediction)
async def generate_prediction(
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        learning_events = await db.learning_events.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(100).to_list(length=100)
        
        import pandas as pd
        if learning_events:
            df = pd.DataFrame(learning_events)
            prediction = learning_predictor.predict(df)
        else:
            prediction = learning_predictor._get_default_prediction()
        
        prediction_dict = {
            "user_id": user_id,
            **prediction,
        }
        
        result = await db.predictions.insert_one(prediction_dict)
        prediction_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Generated prediction for user {user_id}")
        return Prediction(**prediction_dict)
    except Exception as e:
        logger.error(f"Failed to generate prediction: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate prediction")


@router.get("/", response_model=List[Prediction])
async def get_predictions(
    limit: int = 20,
    db=Depends(get_database),
    user_id: str = Depends(get_current_user_id)
):
    try:
        predictions = await db.predictions.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        return [Prediction(**prediction) for prediction in predictions]
    except Exception as e:
        logger.error(f"Failed to get predictions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get predictions")
