from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AgentMemoryBase(BaseModel):
    user_id: str
    agent_name: str
    memory_content: str
    encrypted: bool = False
    context: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = {}


class AgentMemoryCreate(AgentMemoryBase):
    pass


class AgentMemoryInDB(AgentMemoryBase):
    id: str = Field(alias="_id")
    timestamp: datetime
    created_at: datetime

    class Config:
        populate_by_name = True


class AgentMemory(AgentMemoryInDB):
    pass
