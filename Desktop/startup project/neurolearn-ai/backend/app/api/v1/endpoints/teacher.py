from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from loguru import logger
from app.core.database import get_database
from app.models.teacher import (
    CourseCreate, CourseUpdate, CourseResponse,
    NoteCreate, NoteResponse,
    AssignmentCreate, AssignmentResponse,
    StudentProgressCreate, StudentProgressResponse,
    AttendanceRecordCreate, AttendanceRecordResponse,
    BatchCreate, BatchResponse
)
from datetime import datetime
from typing import List

router = APIRouter()
security = HTTPBearer()

@router.post("/courses", response_model=CourseResponse)
async def create_course(course: CourseCreate, token: str = Depends(security)):
    """Create a new course"""
    db = await get_database()
    teacher_id = token.credentials
    
    course_data = course.dict()
    course_data["teacher_id"] = teacher_id
    course_data["created_at"] = datetime.utcnow()
    course_data["updated_at"] = datetime.utcnow()
    
    result = await db.courses.insert_one(course_data)
    course_data["id"] = str(result.inserted_id)
    
    return course_data

@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(token: str = Depends(security)):
    """Get all courses for the teacher"""
    db = await get_database()
    teacher_id = token.credentials
    
    courses = await db.courses.find({"teacher_id": teacher_id}).to_list(50)
    return courses

@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str, token: str = Depends(security)):
    """Get a specific course"""
    db = await get_database()
    
    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(course_id: str, course: CourseUpdate, token: str = Depends(security)):
    """Update a course"""
    db = await get_database()
    
    update_data = {k: v for k, v in course.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.courses.update_one(
        {"id": course_id},
        {"": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return await db.courses.find_one({"id": course_id})

@router.delete("/courses/{course_id}")
async def delete_course(course_id: str, token: str = Depends(security)):
    """Delete a course"""
    db = await get_database()
    
    result = await db.courses.delete_one({"id": course_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {"message": "Course deleted successfully"}

@router.post("/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate, token: str = Depends(security)):
    """Create a new note"""
    db = await get_database()
    teacher_id = token.credentials
    
    note_data = note.dict()
    note_data["teacher_id"] = teacher_id
    note_data["created_at"] = datetime.utcnow()
    note_data["updated_at"] = datetime.utcnow()
    
    result = await db.notes.insert_one(note_data)
    note_data["id"] = str(result.inserted_id)
    
    return note_data

@router.get("/notes", response_model=List[NoteResponse])
async def get_notes(course_id: str = None, token: str = Depends(security)):
    """Get notes for the teacher"""
    db = await get_database()
    teacher_id = token.credentials
    
    query = {"teacher_id": teacher_id}
    if course_id:
        query["course_id"] = course_id
    
    notes = await db.notes.find(query).to_list(50)
    return notes

@router.post("/assignments", response_model=AssignmentResponse)
async def create_assignment(assignment: AssignmentCreate, token: str = Depends(security)):
    """Create a new assignment"""
    db = await get_database()
    teacher_id = token.credentials
    
    assignment_data = assignment.dict()
    assignment_data["teacher_id"] = teacher_id
    assignment_data["created_at"] = datetime.utcnow()
    assignment_data["updated_at"] = datetime.utcnow()
    
    result = await db.assignments.insert_one(assignment_data)
    assignment_data["id"] = str(result.inserted_id)
    
    return assignment_data

@router.get("/assignments", response_model=List[AssignmentResponse])
async def get_assignments(course_id: str = None, token: str = Depends(security)):
    """Get assignments for the teacher"""
    db = await get_database()
    teacher_id = token.credentials
    
    query = {"teacher_id": teacher_id}
    if course_id:
        query["course_id"] = course_id
    
    assignments = await db.assignments.find(query).to_list(50)
    return assignments

@router.get("/students/progress", response_model=List[StudentProgressResponse])
async def get_student_progress(course_id: str, token: str = Depends(security)):
    """Get progress of all students in a course"""
    db = await get_database()
    teacher_id = token.credentials
    
    progress = await db.student_progress.find({
        "teacher_id": teacher_id,
        "course_id": course_id
    }).to_list(50)
    
    return progress

@router.post("/attendance", response_model=AttendanceRecordResponse)
async def record_attendance(record: AttendanceRecordCreate, token: str = Depends(security)):
    """Record student attendance"""
    db = await get_database()
    teacher_id = token.credentials
    
    record_data = record.dict()
    record_data["teacher_id"] = teacher_id
    record_data["created_at"] = datetime.utcnow()
    
    result = await db.attendance_records.insert_one(record_data)
    record_data["id"] = str(result.inserted_id)
    
    return record_data

@router.get("/attendance", response_model=List[AttendanceRecordResponse])
async def get_attendance(course_id: str, date: str = None, token: str = Depends(security)):
    """Get attendance records"""
    db = await get_database()
    teacher_id = token.credentials
    
    query = {"teacher_id": teacher_id, "course_id": course_id}
    if date:
        query["date"] = datetime.fromisoformat(date)
    
    records = await db.attendance_records.find(query).to_list(100)
    return records

@router.post("/batches", response_model=BatchResponse)
async def create_batch(batch: BatchCreate, token: str = Depends(security)):
    """Create a new batch"""
    db = await get_database()
    teacher_id = token.credentials
    
    batch_data = batch.dict()
    batch_data["teacher_id"] = teacher_id
    batch_data["created_at"] = datetime.utcnow()
    batch_data["updated_at"] = datetime.utcnow()
    
    result = await db.batches.insert_one(batch_data)
    batch_data["id"] = str(result.inserted_id)
    
    return batch_data

@router.get("/batches", response_model=List[BatchResponse])
async def get_batches(token: str = Depends(security)):
    """Get all batches for the teacher"""
    db = await get_database()
    teacher_id = token.credentials
    
    batches = await db.batches.find({"teacher_id": teacher_id}).to_list(50)
    return batches

@router.post("/generate-question-paper")
async def generate_question_paper(
    course_id: str,
    topic: str,
    difficulty: str = "medium",
    num_questions: int = 10,
    token: str = Depends(security)
):
    """Generate AI-powered question paper"""
    db = await get_database()
    teacher_id = token.credentials
    
    # This would integrate with the AI agents to generate questions
    # For now, return a placeholder response
    return {
        "course_id": course_id,
        "topic": topic,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "questions": [
            {
                "question": f"Sample question about {topic}",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "marks": 5
            }
        ]
    }

@router.get("/analytics/performance")
async def get_class_performance(course_id: str, token: str = Depends(security)):
    """Get class performance analytics"""
    db = await get_database()
    teacher_id = token.credentials
    
    progress = await db.student_progress.find({
        "teacher_id": teacher_id,
        "course_id": course_id
    }).to_list(50)
    
    if not progress:
        return {"message": "No student progress data available"}
    
    avg_score = sum(p["average_score"] for p in progress) / len(progress)
    avg_attendance = sum(p["attendance_percentage"] for p in progress) / len(progress)
    
    return {
        "course_id": course_id,
        "total_students": len(progress),
        "average_score": avg_score,
        "average_attendance": avg_attendance,
        "students": progress
    }
