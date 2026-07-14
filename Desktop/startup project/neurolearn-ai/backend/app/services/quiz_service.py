from datetime import datetime
from typing import Optional, List
from app.models.quiz import QuizCreate, QuizUpdate, QuizInDB, QuizResponse, QuizAttemptCreate, QuizAttemptInDB
from app.core.database import get_database
from loguru import logger


class QuizService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_quiz(self, quiz_data: QuizCreate) -> QuizInDB:
        db = await self.get_database()
        quiz_dict = quiz_data.model_dump()
        quiz_dict["created_at"] = datetime.utcnow()
        quiz_dict["updated_at"] = datetime.utcnow()
        
        result = await db.quizzes.insert_one(quiz_dict)
        quiz_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Quiz created with ID: {result.inserted_id}")
        return QuizInDB(**quiz_dict)

    async def get_quiz_by_id(self, quiz_id: str) -> Optional[QuizInDB]:
        db = await self.get_database()
        quiz_doc = await db.quizzes.find_one({"_id": quiz_id})
        
        if quiz_doc:
            quiz_doc["_id"] = str(quiz_doc["_id"])
            return QuizInDB(**quiz_doc)
        return None

    async def get_user_quizzes(self, user_id: str, skip: int = 0, limit: int = 20) -> List[QuizInDB]:
        db = await self.get_database()
        cursor = db.quizzes.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
        quizzes = await cursor.to_list(length=limit)
        
        for quiz in quizzes:
            quiz["_id"] = str(quiz["_id"])
        
        return [QuizInDB(**quiz) for quiz in quizzes]

    async def update_quiz(self, quiz_id: str, quiz_update: QuizUpdate, user_id: str) -> Optional[QuizInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in quiz_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.quizzes.update_one(
            {"_id": quiz_id, "user_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_quiz_by_id(quiz_id)
        return None

    async def delete_quiz(self, quiz_id: str, user_id: str) -> bool:
        db = await self.get_database()
        result = await db.quizzes.delete_one({"_id": quiz_id, "user_id": user_id})
        return result.deleted_count > 0

    async def create_quiz_attempt(self, attempt_data: QuizAttemptCreate) -> QuizAttemptInDB:
        db = await self.get_database()
        attempt_dict = attempt_data.model_dump()
        attempt_dict["created_at"] = datetime.utcnow()
        
        result = await db.quiz_attempts.insert_one(attempt_dict)
        attempt_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Quiz attempt created with ID: {result.inserted_id}")
        return QuizAttemptInDB(**attempt_dict)
