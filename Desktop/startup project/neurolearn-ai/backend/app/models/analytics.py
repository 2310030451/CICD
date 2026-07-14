from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SubjectBreakdown(BaseModel):
    subject: str
    total_time: int
    sessions_count: int
    progress: float


class ActivityTimeline(BaseModel):
    date: datetime
    activity_type: str
    description: str
    duration: int


class Prediction(BaseModel):
    predicted_score: float
    confidence: float
    recommendations: List[str]


class AnalyticsBase(BaseModel):
    user_id: str
    date: datetime
    total_study_time: int = 0
    sessions_completed: int = 0
    quizzes_taken: int = 0
    average_quiz_score: float = 0.0
    xp_earned: int = 0


class AnalyticsCreate(AnalyticsBase):
    pass


class AnalyticsInDB(AnalyticsBase):
    id: str = Field(alias="_id")
    subject_breakdown: List[SubjectBreakdown] = []
    activity_timeline: List[ActivityTimeline] = []
    predictions: Optional[Prediction] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Analytics(AnalyticsInDB):
    pass


class AnalyticsResponse(BaseModel):
    id: str
    user_id: str
    date: datetime
    total_study_time: int
    sessions_completed: int
    quizzes_taken: int
    average_quiz_score: float
    xp_earned: int
    subject_breakdown: List[SubjectBreakdown]
    activity_timeline: List[ActivityTimeline]
    predictions: Optional[Prediction] = None
    created_at: datetime
    updated_at: datetime
