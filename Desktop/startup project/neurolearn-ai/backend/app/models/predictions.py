from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PredictionBase(BaseModel):
    user_id: str
    expected_exam_score: float
    weak_topic_score: float
    strong_topic_score: float
    forgetting_probability: float
    failing_risk: float
    learning_speed: str
    future_trend: str
    recommended_revision_time: int
    confidence: float
    prediction_date: datetime


class PredictionCreate(PredictionBase):
    pass


class PredictionInDB(PredictionBase):
    id: str = Field(alias="_id")
    created_at: datetime

    class Config:
        populate_by_name = True


class Prediction(PredictionInDB):
    pass
