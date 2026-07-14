from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class SessionBase(BaseModel):
    user_id: str
    content_id: Optional[str] = None
    title: str
    agent_type: str = "tutor"
    status: SessionStatus = SessionStatus.ACTIVE


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[SessionStatus] = None


class SessionInDB(SessionBase):
    id: str = Field(alias="_id")
    messages: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class Session(SessionInDB):
    pass


class SessionResponse(BaseModel):
    id: str
    user_id: str
    content_id: Optional[str] = None
    title: str
    agent_type: str
    status: SessionStatus
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
