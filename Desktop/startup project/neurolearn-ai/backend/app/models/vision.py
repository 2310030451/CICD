from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ImageType(str, Enum):
    HANDWRITTEN_NOTES = "handwritten_notes"
    MATH_EQUATION = "math_equation"
    FLOWCHART = "flowchart"
    GRAPH = "graph"
    BIOLOGY_DIAGRAM = "biology_diagram"
    CHEMISTRY_STRUCTURE = "chemistry_structure"
    PHYSICS_CIRCUIT = "physics_circuit"
    TABLE = "table"
    CHART = "chart"
    PRINTED_TEXT = "printed_text"
    WHITEBOARD = "whiteboard"
    SCREENSHOT = "screenshot"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VisionImageBase(BaseModel):
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


class VisionImageCreate(VisionImageBase):
    pass


class VisionImageUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class VisionImageInDB(VisionImageBase):
    id: str = Field(alias="_id")
    status: ProcessingStatus = ProcessingStatus.PENDING
    image_type: Optional[ImageType] = None
    classification_confidence: float = 0.0
    ocr_text: Optional[str] = None
    ocr_confidence: float = 0.0
    layout_analysis: Optional[Dict[str, Any]] = None
    image_quality: Optional[Dict[str, float]] = None
    ai_explanation: Optional[str] = None
    generated_quiz: Optional[Dict[str, Any]] = None
    generated_flashcards: Optional[List[Dict[str, Any]]] = None
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class VisionImage(VisionImageInDB):
    pass


class VisionImageResponse(BaseModel):
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
    status: ProcessingStatus
    image_type: Optional[ImageType] = None
    classification_confidence: float
    ocr_text: Optional[str] = None
    ocr_confidence: float
    layout_analysis: Optional[Dict[str, Any]] = None
    image_quality: Optional[Dict[str, float]] = None
    ai_explanation: Optional[str] = None
    generated_quiz: Optional[Dict[str, Any]] = None
    generated_flashcards: Optional[List[Dict[str, Any]]] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
