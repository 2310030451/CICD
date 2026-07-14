from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class RecommendationBase(BaseModel):
    user_id: str
    recommendation_type: str
    topics_to_revise: List[Dict[str, Any]] = []
    practice_questions: List[Dict[str, Any]] = []
    study_schedule: Dict[str, Any] = {}
    difficulty_adjustment: Dict[str, Any] = {}
    learning_resources: List[Dict[str, Any]] = []
    confidence: float = 0.5
    generated_at: datetime
    metadata: Dict[str, Any] = {}


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationInDB(RecommendationBase):
    id: str = Field(alias="_id")
    created_at: datetime

    class Config:
        populate_by_name = True


class Recommendation(RecommendationInDB):
    pass
