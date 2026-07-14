from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from app.models.document import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentStatus
from app.services.document_service import DocumentService
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


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
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
        allowed_types = settings.allowed_file_types.split(",")
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_extension} not allowed"
            )

        file_content = await file.read()
        
        if len(file_content) > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum of {settings.max_file_size} bytes"
            )

        file_hash = calculate_file_hash(file_content)
        
        os.makedirs(settings.upload_directory, exist_ok=True)
        
        file_path = os.path.join(settings.upload_directory, f"{file_hash}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(file_content)

        file_url = f"/uploads/{file_hash}_{file.filename}"
        
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        document_service = DocumentService()
        document_data = DocumentCreate(
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
        
        document = await document_service.create_document(document_data)
        
        await document_service.process_document(document.id)
        
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document"
        )


@router.get("/", response_model=List[DocumentResponse])
async def get_user_documents(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[DocumentStatus] = None
):
    document_service = DocumentService()
    documents = await document_service.get_user_documents(
        user_id, skip, limit, status_filter
    )
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    user_id: str = Depends(get_current_user_id)
):
    document_service = DocumentService()
    document = await document_service.get_document_by_id(document_id, user_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    user_id: str = Depends(get_current_user_id)
):
    document_service = DocumentService()
    document = await document_service.update_document(document_id, document_update, user_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user_id: str = Depends(get_current_user_id)
):
    document_service = DocumentService()
    success = await document_service.delete_document(document_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return {"message": "Document deleted successfully"}
