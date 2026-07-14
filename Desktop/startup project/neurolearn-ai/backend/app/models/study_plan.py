from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PlanStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class StudyPlanBase(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    subjects: List[str] = []
    daily_hours: float = 4.0
    goals: List[str] = []
    schedule: Dict[str, Any] = {}
    status: PlanStatus = PlanStatus.ACTIVE
    metadata: Dict[str, Any] = {}


class StudyPlanCreate(StudyPlanBase):
    pass


class StudyPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    subjects: Optional[List[str]] = None
    daily_hours: Optional[float] = None
    goals: Optional[List[str]] = None
    schedule: Optional[Dict[str, Any]] = None
    status: Optional[PlanStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class StudyPlanInDB(StudyPlanBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class StudyPlan(StudyPlanInDB):
    pass
