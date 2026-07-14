from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class SubscriptionTier(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"


class UserBase(BaseModel):
    firebase_uid: str
    email: EmailStr
    display_name: str
    role: UserRole = UserRole.STUDENT
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    is_active: bool = True
    is_verified: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    role: Optional[UserRole] = None
    subscription_tier: Optional[SubscriptionTier] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    photo_url: Optional[str] = None


class UserInDB(UserBase):
    id: str = Field(alias="_id")
    photo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        populate_by_name = True


class User(UserInDB):
    pass


class UserResponse(BaseModel):
    id: str
    firebase_uid: str
    email: str
    display_name: str
    role: UserRole
    subscription_tier: SubscriptionTier
    photo_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
