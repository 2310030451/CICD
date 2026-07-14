from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.quiz import QuizCreate, QuizUpdate, QuizResponse, QuizAttemptCreate, QuizAttempt
from app.services.quiz_service import QuizService
from app.core.auth import decode_token
from loguru import logger

router = APIRouter()


async def get_current_user_id(token: str) -> str:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return payload.get("user_id")


@router.post("/", response_model=QuizResponse)
async def create_quiz(
    quiz: QuizCreate,
    user_id: str = Depends(get_current_user_id)
):
    quiz_service = QuizService()
    quiz.user_id = user_id
    created_quiz = await quiz_service.create_quiz(quiz)
    return created_quiz


@router.get("/", response_model=List[QuizResponse])
async def get_user_quizzes(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 20
):
    quiz_service = QuizService()
    quizzes = await quiz_service.get_user_quizzes(user_id, skip, limit)
    return quizzes


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: str):
    quiz_service = QuizService()
    quiz = await quiz_service.get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz


@router.put("/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: str,
    quiz_update: QuizUpdate,
    user_id: str = Depends(get_current_user_id)
):
    quiz_service = QuizService()
    quiz = await quiz_service.update_quiz(quiz_id, quiz_update, user_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    user_id: str = Depends(get_current_user_id)
):
    quiz_service = QuizService()
    success = await quiz_service.delete_quiz(quiz_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return {"message": "Quiz deleted successfully"}


@router.post("/{quiz_id}/attempts", response_model=QuizAttempt)
async def submit_quiz_attempt(
    quiz_id: str,
    attempt: QuizAttemptCreate,
    user_id: str = Depends(get_current_user_id)
):
    quiz_service = QuizService()
    attempt.user_id = user_id
    attempt.quiz_id = quiz_id
    created_attempt = await quiz_service.create_quiz_attempt(attempt)
    return created_attempt
