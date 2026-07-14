from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QuizDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    FILL_BLANK = "fill_blank"


class QuestionBase(BaseModel):
    question_text: str
    question_type: QuestionType
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    points: int = 10


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True


class QuizBase(BaseModel):
    user_id: str
    content_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    difficulty: QuizDifficulty = QuizDifficulty.MEDIUM
    questions: List[QuestionCreate] = []
    time_limit: Optional[int] = None
    passing_score: int = 70


class QuizCreate(QuizBase):
    pass


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[QuizDifficulty] = None
    time_limit: Optional[int] = None
    passing_score: Optional[int] = None


class QuizInDB(QuizBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Quiz(QuizInDB):
    pass


class QuizResponse(BaseModel):
    id: str
    user_id: str
    content_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    difficulty: QuizDifficulty
    questions: List[Question]
    time_limit: Optional[int] = None
    passing_score: int
    created_at: datetime
    updated_at: datetime


class QuizAttemptBase(BaseModel):
    user_id: str
    quiz_id: str
    answers: Dict[str, Any]
    score: int
    passed: bool
    time_taken: int


class QuizAttemptCreate(QuizAttemptBase):
    pass


class QuizAttemptInDB(QuizAttemptBase):
    id: str = Field(alias="_id")
    created_at: datetime

    class Config:
        populate_by_name = True


class QuizAttempt(QuizAttemptInDB):
    pass
