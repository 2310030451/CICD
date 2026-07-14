from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ParentChildRelationBase(BaseModel):
    parent_id: str
    child_id: str
    relationship: str  # father, mother, guardian
    is_primary: bool = True

class ParentChildRelationCreate(ParentChildRelationBase):
    pass

class ParentChildRelationDB(ParentChildRelationBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class ParentChildRelationResponse(ParentChildRelationDB):
    pass

class StudentProgressReportBase(BaseModel):
    parent_id: str
    child_id: str
    period: str  # weekly, monthly, semester
    exam_predictions: dict
    weak_subjects: List[str]
    strong_subjects: List[str]
    study_hours: float
    attendance_percentage: float
    average_score: float
    ai_suggestions: List[str]
    generated_at: datetime

class StudentProgressReportCreate(StudentProgressReportBase):
    pass

class StudentProgressReportDB(StudentProgressReportBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class StudentProgressReportResponse(StudentProgressReportDB):
    pass

class ParentNotificationBase(BaseModel):
    parent_id: str
    child_id: str
    title: str
    message: str
    type: str  # attendance, grade, behavior, system
    is_read: bool = False

class ParentNotificationCreate(ParentNotificationBase):
    pass

class ParentNotificationDB(ParentNotificationBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class ParentNotificationResponse(ParentNotificationDB):
    pass

class RevisionCalendarBase(BaseModel):
    parent_id: str
    child_id: str
    subject: str
    topic: str
    scheduled_date: datetime
    priority: str  # high, medium, low
    status: str  # pending, completed, skipped

class RevisionCalendarCreate(RevisionCalendarBase):
    pass

class RevisionCalendarDB(RevisionCalendarBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class RevisionCalendarResponse(RevisionCalendarDB):
    pass
