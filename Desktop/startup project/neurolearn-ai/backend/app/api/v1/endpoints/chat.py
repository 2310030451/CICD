from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
from app.models.conversation import ConversationCreate, ConversationUpdate, ConversationResponse
from app.services.conversation_service import ConversationService
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


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    document_ids: Optional[List[str]] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    conversation_id: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    try:
        conversation_service = ConversationService()
        
        if not request.conversation_id:
            conversation = await conversation_service.create_conversation(
                ConversationCreate(
                    user_id=user_id,
                    title=request.question[:50],
                    document_ids=request.document_ids or [],
                )
            )
            request.conversation_id = str(conversation.id)
        
        response = await conversation_service.chat(
            conversation_id=request.conversation_id,
            question=request.question,
            user_id=user_id,
            document_ids=request.document_ids,
        )
        
        return ChatResponse(
            answer=response["answer"],
            sources=response["sources"],
            conversation_id=request.conversation_id,
        )
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id)
):
    async def generate():
        try:
            conversation_service = ConversationService()
            
            if not request.conversation_id:
                conversation = await conversation_service.create_conversation(
                    ConversationCreate(
                        user_id=user_id,
                        title=request.question[:50],
                        document_ids=request.document_ids or [],
                    )
                )
                request.conversation_id = str(conversation.id)
            
            async for chunk in conversation_service.chat_stream(
                conversation_id=request.conversation_id,
                question=request.question,
                user_id=user_id,
                document_ids=request.document_ids,
            ):
                yield chunk
        except Exception as e:
            logger.error(f"Streaming chat failed: {e}")
            yield f"Error: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 20
):
    conversation_service = ConversationService()
    conversations = await conversation_service.get_user_conversations(user_id, skip, limit)
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id)
):
    conversation_service = ConversationService()
    conversation = await conversation_service.get_conversation_by_id(conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id)
):
    conversation_service = ConversationService()
    success = await conversation_service.delete_conversation(conversation_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return {"message": "Conversation deleted successfully"}
