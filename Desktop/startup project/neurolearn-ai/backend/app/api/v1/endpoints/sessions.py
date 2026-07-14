from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.session import SessionCreate, SessionUpdate, SessionResponse
from app.services.session_service import SessionService
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


@router.post("/", response_model=SessionResponse)
async def create_session(
    session: SessionCreate,
    user_id: str = Depends(get_current_user_id)
):
    session_service = SessionService()
    session.user_id = user_id
    created_session = await session_service.create_session(session)
    return created_session


@router.get("/", response_model=List[SessionResponse])
async def get_user_sessions(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 20
):
    session_service = SessionService()
    sessions = await session_service.get_user_sessions(user_id, skip, limit)
    return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    session_service = SessionService()
    session = await session_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    session_update: SessionUpdate,
    user_id: str = Depends(get_current_user_id)
):
    session_service = SessionService()
    session = await session_service.update_session(session_id, session_update, user_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    user_id: str = Depends(get_current_user_id)
):
    session_service = SessionService()
    success = await session_service.delete_session(session_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return {"message": "Session deleted successfully"}
