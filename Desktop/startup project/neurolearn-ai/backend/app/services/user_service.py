from datetime import datetime
from typing import Optional
from app.models.user import UserCreate, UserUpdate, UserInDB, UserResponse
from app.core.database import get_database
from loguru import logger


class UserService:
    def __init__(self):
        self.db = None

    async def get_database(self):
        if not self.db:
            self.db = await get_database()
        return self.db

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        db = await self.get_database()
        user_dict = user_data.model_dump()
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        logger.info(f"User created with ID: {result.inserted_id}")
        return UserInDB(**user_dict)

    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[UserInDB]:
        db = await self.get_database()
        user_doc = await db.users.find_one({"firebase_uid": firebase_uid})
        
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        db = await self.get_database()
        user_doc = await db.users.find_one({"_id": user_id})
        
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        db = await self.get_database()
        user_doc = await db.users.find_one({"email": email})
        
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])
            return UserInDB(**user_doc)
        return None

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
        db = await self.get_database()
        update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.users.update_one(
            {"_id": user_id},
            {"": update_data}
        )
        
        if result.modified_count > 0:
            return await self.get_user_by_id(user_id)
        return None

    async def get_or_create_user(self, firebase_user: dict) -> UserInDB:
        firebase_uid = firebase_user.get("uid")
        user = await self.get_user_by_firebase_uid(firebase_uid)
        
        if user:
            await db.users.update_one(
                {"_id": user.id},
                {"": {"last_login": datetime.utcnow()}}
            )
            return user
        
        user_data = UserCreate(
            firebase_uid=firebase_uid,
            email=firebase_user.get("email"),
            display_name=firebase_user.get("displayName", firebase_user.get("email").split("@")[0]),
            photo_url=firebase_user.get("photoURL"),
            is_verified=firebase_user.get("emailVerified", False)
        )
        
        return await self.create_user(user_data)
