from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class CourseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class AssignmentType(str, Enum):
    HOMEWORK = "homework"
    QUIZ = "quiz"
    PROJECT = "project"
    EXAM = "exam"

class CourseBase(BaseModel):
    teacher_id: str
    title: str
    description: str
    subject: str
    grade_level: str
    status: CourseStatus = CourseStatus.DRAFT
    enrolled_students: List[str] = []

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    grade_level: Optional[str] = None
    status: Optional[CourseStatus] = None
    enrolled_students: Optional[List[str]] = None

class CourseDB(CourseBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class CourseResponse(CourseDB):
    pass

class NoteBase(BaseModel):
    teacher_id: str
    course_id: str
    title: str
    content: str
    topic: str

class NoteCreate(NoteBase):
    pass

class NoteDB(NoteBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class NoteResponse(NoteDB):
    pass

class AssignmentBase(BaseModel):
    teacher_id: str
    course_id: str
    title: str
    description: str
    assignment_type: AssignmentType
    due_date: datetime
    max_points: int
    questions: Optional[List[dict]] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentDB(AssignmentBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class AssignmentResponse(AssignmentDB):
    pass

class StudentProgressBase(BaseModel):
    teacher_id: str
    student_id: str
    course_id: str
    average_score: float
    assignments_completed: int
    total_assignments: int
    attendance_percentage: float
    last_active: datetime

class StudentProgressCreate(StudentProgressBase):
    pass

class StudentProgressDB(StudentProgressBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class StudentProgressResponse(StudentProgressDB):
    pass

class AttendanceRecordBase(BaseModel):
    teacher_id: str
    course_id: str
    student_id: str
    date: datetime
    status: str  # present, absent, late
    notes: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordDB(AttendanceRecordBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class AttendanceRecordResponse(AttendanceRecordDB):
    pass

class BatchBase(BaseModel):
    teacher_id: str
    name: str
    grade_level: str
    subject: str
    student_ids: List[str] = []

class BatchCreate(BatchBase):
    pass

class BatchDB(BatchBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow())
    updated_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class BatchResponse(BatchDB):
    pass
