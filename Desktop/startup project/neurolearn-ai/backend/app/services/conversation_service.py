from datetime import datetime
from typing import Optional, List, AsyncGenerator
from app.models.conversation import ConversationCreate, ConversationUpdate, ConversationInDB, MessageCreate, MessageRole
from app.core.database import get_database
from app.ai.rag import rag_pipeline
from loguru import logger


class ConversationService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_conversation(self, conversation_data: ConversationCreate) -> ConversationInDB:
        db = await self.get_database()
        conversation_dict = conversation_data.model_dump()
        conversation_dict["messages"] = []
        conversation_dict["metadata"] = {}
        conversation_dict["created_at"] = datetime.utcnow()
        conversation_dict["updated_at"] = datetime.utcnow()
        
        result = await db.conversations.insert_one(conversation_dict)
        conversation_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Conversation created with ID: {result.inserted_id}")
        return ConversationInDB(**conversation_dict)

    async def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Optional[ConversationInDB]:
        db = await self.get_database()
        conversation_doc = await db.conversations.find_one({"_id": conversation_id, "user_id": user_id})
        
        if conversation_doc:
            conversation_doc["_id"] = str(conversation_doc["_id"])
            return ConversationInDB(**conversation_doc)
        return None

    async def get_user_conversations(self, user_id: str, skip: int = 0, limit: int = 20) -> List[ConversationInDB]:
        db = await self.get_database()
        cursor = db.conversations.find({"user_id": user_id}).sort("updated_at", -1).skip(skip).limit(limit)
        conversations = await cursor.to_list(length=limit)
        
        for conversation in conversations:
            conversation["_id"] = str(conversation["_id"])
        
        return [ConversationInDB(**conversation) for conversation in conversations]

    async def update_conversation(self, conversation_id: str, conversation_update: ConversationUpdate, user_id: str) -> Optional[ConversationInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in conversation_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.conversations.update_one(
            {"_id": conversation_id, "user_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_conversation_by_id(conversation_id, user_id)
        return None

    async def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        db = await self.get_database()
        result = await db.conversations.delete_one({"_id": conversation_id, "user_id": user_id})
        return result.deleted_count > 0

    async def add_message(
        self,
        conversation_id: str,
        role: MessageRole,
        content: str,
        sources: List[dict] = None,
    ):
        db = await self.get_database()
        message_dict = {
            "role": role,
            "content": content,
            "sources": sources or [],
            "metadata": {},
            "created_at": datetime.utcnow(),
        }
        
        await db.conversations.update_one(
            {"_id": conversation_id},
            {
                "": {"messages": message_dict},
                "": {"updated_at": datetime.utcnow()},
            }
        )

    async def chat(
        self,
        conversation_id: str,
        question: str,
        user_id: str,
        document_ids: Optional[List[str]] = None,
    ) -> dict:
        try:
            await self.add_message(conversation_id, MessageRole.USER, question)
            
            response = await rag_pipeline.query(
                question=question,
                user_id=user_id,
                conversation_id=conversation_id,
                document_ids=document_ids,
            )
            
            await self.add_message(
                conversation_id,
                MessageRole.ASSISTANT,
                response["answer"],
                response["sources"],
            )
            
            return response
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            raise

    async def chat_stream(
        self,
        conversation_id: str,
        question: str,
        user_id: str,
        document_ids: Optional[List[str]] = None,
    ) -> AsyncGenerator[str, None]:
        try:
            await self.add_message(conversation_id, MessageRole.USER, question)
            
            full_response = ""
            sources = []
            
            async for chunk in rag_pipeline.query_stream(
                question=question,
                user_id=user_id,
                conversation_id=conversation_id,
                document_ids=document_ids,
            ):
                full_response += chunk
                yield chunk
            
            await self.add_message(
                conversation_id,
                MessageRole.ASSISTANT,
                full_response,
                sources,
            )
        except Exception as e:
            logger.error(f"Streaming chat failed: {e}")
            raise
