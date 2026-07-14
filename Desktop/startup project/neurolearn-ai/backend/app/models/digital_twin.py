from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class LearningStyle(str, Enum):
    TEXT = "text"
    DIAGRAM = "diagram"
    FLASHCARDS = "flashcards"
    VIDEOS = "videos"
    PRACTICE_QUESTIONS = "practice_questions"
    MIXED = "mixed"


class StudyTimePreference(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    FLEXIBLE = "flexible"


class DigitalTwinBase(BaseModel):
    user_id: str
    learning_style: LearningStyle
    learning_speed: str
    attention_span_minutes: int
    knowledge_gaps: List[Dict[str, Any]] = []
    revision_patterns: Dict[str, Any] = {}
    preferred_study_time: StudyTimePreference
    confidence_level: float
    memory_retention: float
    strengths: List[Dict[str, Any]] = []
    weaknesses: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}


class DigitalTwinCreate(DigitalTwinBase):
    pass


class DigitalTwinUpdate(BaseModel):
    learning_style: Optional[LearningStyle] = None
    learning_speed: Optional[str] = None
    attention_span_minutes: Optional[int] = None
    knowledge_gaps: Optional[List[Dict[str, Any]]] = None
    revision_patterns: Optional[Dict[str, Any]] = None
    preferred_study_time: Optional[StudyTimePreference] = None
    confidence_level: Optional[float] = None
    memory_retention: Optional[float] = None
    strengths: Optional[List[Dict[str, Any]]] = None
    weaknesses: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class DigitalTwinInDB(DigitalTwinBase):
    id: str = Field(alias="_id")
    last_updated: datetime
    created_at: datetime

    class Config:
        populate_by_name = True


class DigitalTwin(DigitalTwinInDB):
    pass
