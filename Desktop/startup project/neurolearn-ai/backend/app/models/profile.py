from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProfileBase(BaseModel):
    user_id: str
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    interests: List[str] = []
    learning_goals: List[str] = []


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    interests: Optional[List[str]] = None
    learning_goals: Optional[List[str]] = None


class ProfileInDB(ProfileBase):
    id: str = Field(alias="_id")
    xp: int = 0
    level: int = 1
    streak: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class Profile(ProfileInDB):
    pass


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    interests: List[str] = []
    learning_goals: List[str] = []
    xp: int
    level: int
    streak: int
    created_at: datetime
    updated_at: datetime
