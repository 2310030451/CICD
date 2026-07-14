from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentBase(BaseModel):
    user_id: str
    title: str
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    file_hash: str
    subject: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentInDB(DocumentBase):
    id: str = Field(alias="_id")
    status: DocumentStatus = DocumentStatus.PROCESSING
    text_content: Optional[str] = None
    chunk_count: int = 0
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Document(DocumentInDB):
    pass


class DocumentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    file_hash: str
    subject: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any]
    status: DocumentStatus
    chunk_count: int
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
