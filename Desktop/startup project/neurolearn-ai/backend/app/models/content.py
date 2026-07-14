from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "markdown"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    WEBPAGE = "webpage"


class ContentBase(BaseModel):
    user_id: str
    title: str
    content_type: ContentType
    file_url: str
    file_size: int
    file_hash: str
    metadata: Dict[str, Any] = {}
    tags: List[str] = []
    subject: Optional[str] = None


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    subject: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ContentInDB(ContentBase):
    id: str = Field(alias="_id")
    summary: Optional[str] = None
    key_concepts: List[str] = []
    processed: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Content(ContentInDB):
    pass


class ContentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content_type: ContentType
    file_url: str
    file_size: int
    file_hash: str
    metadata: Dict[str, Any]
    tags: List[str]
    subject: Optional[str] = None
    summary: Optional[str] = None
    key_concepts: List[str]
    processed: bool
    created_at: datetime
    updated_at: datetime
