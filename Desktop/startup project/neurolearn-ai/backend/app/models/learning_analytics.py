from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class LearningEventType(str, Enum):
    QUIZ_ATTEMPT = "quiz_attempt"
    DOCUMENT_UPLOAD = "document_upload"
    CHAT_INTERACTION = "chat_interaction"
    VISION_IMAGE_UPLOAD = "vision_image_upload"
    STUDY_SESSION = "study_session"
    REVISION_SESSION = "revision_session"
    FLASHCARD_PRACTICE = "flashcard_practice"
    CODE_PRACTICE = "code_practice"


class LearningEventBase(BaseModel):
    user_id: str
    event_type: LearningEventType
    topic: Optional[str] = None
    subject: Optional[str] = None
    duration: int = 0
    score: Optional[float] = None
    metadata: Dict[str, Any] = {}


class LearningEventCreate(LearningEventBase):
    pass


class LearningEventInDB(LearningEventBase):
    id: str = Field(alias="_id")
    timestamp: datetime
    created_at: datetime

    class Config:
        populate_by_name = True


class LearningEvent(LearningEventInDB):
    pass


class AnalyticsPeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AnalyticsBase(BaseModel):
    user_id: str
    period: AnalyticsPeriod
    start_date: datetime
    end_date: datetime
    total_study_time: int = 0
    total_quizzes: int = 0
    average_score: float = 0.0
    topics_covered: List[str] = []
    streak_days: int = 0
    xp_earned: int = 0
    metadata: Dict[str, Any] = {}


class AnalyticsCreate(AnalyticsBase):
    pass


class AnalyticsInDB(AnalyticsBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Analytics(AnalyticsInDB):
    pass
