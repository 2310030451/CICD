from datetime import datetime
from typing import Optional, List
from app.models.session import SessionCreate, SessionUpdate, SessionInDB, SessionResponse
from app.core.database import get_database
from loguru import logger


class SessionService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_session(self, session_data: SessionCreate) -> SessionInDB:
        db = await self.get_database()
        session_dict = session_data.model_dump()
        session_dict["created_at"] = datetime.utcnow()
        session_dict["updated_at"] = datetime.utcnow()
        
        result = await db.sessions.insert_one(session_dict)
        session_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Session created with ID: {result.inserted_id}")
        return SessionInDB(**session_dict)

    async def get_session_by_id(self, session_id: str) -> Optional[SessionInDB]:
        db = await self.get_database()
        session_doc = await db.sessions.find_one({"_id": session_id})
        
        if session_doc:
            session_doc["_id"] = str(session_doc["_id"])
            return SessionInDB(**session_doc)
        return None

    async def get_user_sessions(self, user_id: str, skip: int = 0, limit: int = 20) -> List[SessionInDB]:
        db = await self.get_database()
        cursor = db.sessions.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
        sessions = await cursor.to_list(length=limit)
        
        for session in sessions:
            session["_id"] = str(session["_id"])
        
        return [SessionInDB(**session) for session in sessions]

    async def update_session(self, session_id: str, session_update: SessionUpdate, user_id: str) -> Optional[SessionInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in session_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        if session_update.status == "completed":
            update_data["completed_at"] = datetime.utcnow()
        
        result = await db.sessions.update_one(
            {"_id": session_id, "user_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_session_by_id(session_id)
        return None

    async def delete_session(self, session_id: str, user_id: str) -> bool:
        db = await self.get_database()
        result = await db.sessions.delete_one({"_id": session_id, "user_id": user_id})
        return result.deleted_count > 0
