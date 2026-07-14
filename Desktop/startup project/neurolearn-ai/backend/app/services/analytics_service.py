from datetime import datetime, timedelta
from typing import Optional, List
from app.models.analytics import AnalyticsCreate, AnalyticsInDB, AnalyticsResponse
from app.core.database import get_database
from loguru import logger


class AnalyticsService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_analytics(self, analytics_data: AnalyticsCreate) -> AnalyticsInDB:
        db = await self.get_database()
        analytics_dict = analytics_data.model_dump()
        analytics_dict["created_at"] = datetime.utcnow()
        analytics_dict["updated_at"] = datetime.utcnow()
        
        result = await db.analytics.insert_one(analytics_dict)
        analytics_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"Analytics created with ID: {result.inserted_id}")
        return AnalyticsInDB(**analytics_dict)

    async def get_analytics_by_id(self, analytics_id: str) -> Optional[AnalyticsInDB]:
        db = await self.get_database()
        analytics_doc = await db.analytics.find_one({"_id": analytics_id})
        
        if analytics_doc:
            analytics_doc["_id"] = str(analytics_doc["_id"])
            return AnalyticsInDB(**analytics_doc)
        return None

    async def get_user_analytics(self, user_id: str, skip: int = 0, limit: int = 30) -> List[AnalyticsInDB]:
        db = await self.get_database()
        cursor = db.analytics.find({"user_id": user_id}).sort("date", -1).skip(skip).limit(limit)
        analytics_list = await cursor.to_list(length=limit)
        
        for analytics in analytics_list:
            analytics["_id"] = str(analytics["_id"])
        
        return [AnalyticsInDB(**analytics) for analytics in analytics_list]

    async def get_analytics_summary(self, user_id: str) -> dict:
        db = await self.get_database()
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        pipeline = [
            {"": {"user_id": user_id, "date": {"": thirty_days_ago}}},
            {
                "": {
                    "_id": None,
                    "total_study_time": {"": ""},
                    "total_sessions": {"": ""},
                    "total_quizzes": {"": ""},
                    "total_xp": {"": ""},
                    "avg_score": {"": ""}
                }
            }
        ]
        
        result = await db.analytics.aggregate(pipeline).to_list(length=1)
        
        if result:
            return {
                "total_study_time": result[0].get("total_study_time", 0),
                "total_sessions": result[0].get("total_sessions", 0),
                "total_quizzes": result[0].get("total_quizzes", 0),
                "total_xp": result[0].get("total_xp", 0),
                "average_quiz_score": round(result[0].get("avg_score", 0), 2)
            }
        
        return {
            "total_study_time": 0,
            "total_sessions": 0,
            "total_quizzes": 0,
            "total_xp": 0,
            "average_quiz_score": 0
        }
