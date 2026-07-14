from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from app.models.content import ContentCreate, ContentUpdate, ContentResponse
from app.services.content_service import ContentService
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


@router.post("/", response_model=ContentResponse)
async def create_content(
    content: ContentCreate,
    user_id: str = Depends(get_current_user_id)
):
    content_service = ContentService()
    content.user_id = user_id
    created_content = await content_service.create_content(content)
    return created_content


@router.get("/", response_model=List[ContentResponse])
async def get_user_content(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 20
):
    content_service = ContentService()
    contents = await content_service.get_user_contents(user_id, skip, limit)
    return contents


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str):
    content_service = ContentService()
    content = await content_service.get_content_by_id(content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: str,
    content_update: ContentUpdate,
    user_id: str = Depends(get_current_user_id)
):
    content_service = ContentService()
    content = await content_service.update_content(content_id, content_update, user_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return content


@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    user_id: str = Depends(get_current_user_id)
):
    content_service = ContentService()
    success = await content_service.delete_content(content_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    return {"message": "Content deleted successfully"}
