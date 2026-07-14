from datetime import datetime
from typing import Optional, List
from app.models.content import ContentCreate, ContentUpdate, ContentInDB, ContentResponse
from app.core.database import get_database
from loguru import logger


class ContentService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_content(self, content_data: ContentCreate) -> ContentInDB:
        db = await self.get_database()
        content_dict = content_data.model_dump()
        content_dict["created_at"] = datetime.utcnow()
        content_dict["updated_at"] = datetime.utcnow()
        content_dict["processed"] = False
        
        result = await db.content.insert_one(content_dict)
        content_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Content created with ID: {result.inserted_id}")
        return ContentInDB(**content_dict)

    async def get_content_by_id(self, content_id: str) -> Optional[ContentInDB]:
        db = await self.get_database()
        content_doc = await db.content.find_one({"_id": content_id})
        
        if content_doc:
            content_doc["_id"] = str(content_doc["_id"])
            return ContentInDB(**content_doc)
        return None

    async def get_user_contents(self, user_id: str, skip: int = 0, limit: int = 20) -> List[ContentInDB]:
        db = await self.get_database()
        cursor = db.content.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
        contents = await cursor.to_list(length=limit)
        
        for content in contents:
            content["_id"] = str(content["_id"])
        
        return [ContentInDB(**content) for content in contents]

    async def update_content(self, content_id: str, content_update: ContentUpdate, user_id: str) -> Optional[ContentInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in content_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.content.update_one(
            {"_id": content_id, "user_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_content_by_id(content_id)
        return None

    async def delete_content(self, content_id: str, user_id: str) -> bool:
        db = await self.get_database()
        result = await db.content.delete_one({"_id": content_id, "user_id": user_id})
        return result.deleted_count > 0
