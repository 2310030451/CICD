from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageBase(BaseModel):
    role: MessageRole
    content: str
    sources: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True


class ConversationBase(BaseModel):
    user_id: str
    title: str
    document_ids: List[str] = []
    agent_type: str = "tutor"


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    document_ids: Optional[List[str]] = None


class ConversationInDB(ConversationBase):
    id: str = Field(alias="_id")
    messages: List[Message] = []
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Conversation(ConversationInDB):
    pass


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    document_ids: List[str]
    agent_type: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
