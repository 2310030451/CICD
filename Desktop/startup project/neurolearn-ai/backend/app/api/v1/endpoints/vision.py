from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from app.models.vision import VisionImageCreate, VisionImageUpdate, VisionImageResponse, ProcessingStatus
from app.services.vision_service import VisionService
from app.core.auth import decode_token
from loguru import logger
import hashlib
import os
from app.config import settings

router = APIRouter()


async def get_current_user_id(token: str) -> str:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return payload.get("user_id")


def calculate_file_hash(file_content: bytes) -> str:
    return hashlib.sha256(file_content).hexdigest()


@router.post("/upload", response_model=VisionImageResponse)
async def upload_vision_image(
    file: UploadFile = File(...),
    title: str = Form(...),
    subject: Optional[str] = Form(None),
    tags: str = Form(""),
    user_id: str = Depends(get_current_user_id)
):
    try:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )

        file_extension = file.filename.split(".")[-1].lower()
        allowed_types = settings.allowed_image_types.split(",")
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_extension} not allowed"
            )

        file_content = await file.read()
        
        if len(file_content) > settings.image_max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum of {settings.image_max_size} bytes"
            )

        file_hash = calculate_file_hash(file_content)
        
        os.makedirs(settings.upload_directory, exist_ok=True)
        
        file_path = os.path.join(settings.upload_directory, f"{file_hash}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(file_content)

        file_url = f"/uploads/{file_hash}_{file.filename}"
        
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        vision_service = VisionService()
        image_data = VisionImageCreate(
            user_id=user_id,
            title=title,
            file_name=file.filename,
            file_type=file_extension,
            file_size=len(file_content),
            file_url=file_url,
            file_hash=file_hash,
            subject=subject,
            tags=tags_list,
        )
        
        image = await vision_service.create_vision_image(image_data)
        
        await vision_service.process_vision_image(image.id)
        
        return image
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Vision image upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload vision image"
        )


@router.get("/", response_model=List[VisionImageResponse])
async def get_user_vision_images(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[ProcessingStatus] = None
):
    vision_service = VisionService()
    images = await vision_service.get_user_vision_images(
        user_id, skip, limit, status_filter
    )
    return images


@router.get("/{image_id}", response_model=VisionImageResponse)
async def get_vision_image(
    image_id: str,
    user_id: str = Depends(get_current_user_id)
):
    vision_service = VisionService()
    image = await vision_service.get_vision_image_by_id(image_id, user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision image not found"
        )
    return image


@router.put("/{image_id}", response_model=VisionImageResponse)
async def update_vision_image(
    image_id: str,
    image_update: VisionImageUpdate,
    user_id: str = Depends(get_current_user_id)
):
    vision_service = VisionService()
    image = await vision_service.update_vision_image(image_id, image_update, user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision image not found"
        )
    return image


@router.delete("/{image_id}")
async def delete_vision_image(
    image_id: str,
    user_id: str = Depends(get_current_user_id)
):
    vision_service = VisionService()
    success = await vision_service.delete_vision_image(image_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vision image not found"
        )
    return {"message": "Vision image deleted successfully"}


@router.post("/{image_id}/quiz")
async def generate_quiz(
    image_id: str,
    user_id: str = Depends(get_current_user_id)
):
    vision_service = VisionService()
    try:
        quiz = await vision_service.generate_quiz_from_image(image_id, user_id)
        return quiz
    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate quiz"
        )


@router.post("/{image_id}/flashcards")
async def generate_flashcards(
    image_id: str,
    user_id: str = Depends(get_current_user_id)
):
    vision_service = VisionService()
    try:
        flashcards = await vision_service.generate_flashcards_from_image(image_id, user_id)
        return {"flashcards": flashcards}
    except Exception as e:
        logger.error(f"Flashcard generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate flashcards"
        )
