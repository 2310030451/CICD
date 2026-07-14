from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    TEACHER = "teacher"
    PARENT = "parent"
    STUDENT = "student"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class SystemMetricsBase(BaseModel):
    total_users: int
    active_users: int
    total_documents: int
    total_ai_queries: int
    total_vision_queries: int
    revenue_monthly: float
    revenue_total: float
    active_subscriptions: int

class SystemMetricsCreate(SystemMetricsBase):
    pass

class SystemMetricsDB(SystemMetricsBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class SystemMetricsResponse(SystemMetricsDB):
    pass

class AuditLogBase(BaseModel):
    user_id: Optional[str] = None
    action: str
    resource: str
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogDB(AuditLogBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class AuditLogResponse(AuditLogDB):
    pass

class SystemHealthBase(BaseModel):
    service: str
    status: str
    response_time: float
    last_check: datetime

class SystemHealthCreate(SystemHealthBase):
    pass

class SystemHealthDB(SystemHealthBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))

    class Config:
        populate_by_name = True

class SystemHealthResponse(SystemHealthDB):
    pass

class ErrorLogBase(BaseModel):
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    endpoint: Optional[str] = None
    severity: str = "error"

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLogDB(ErrorLogBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    timestamp: datetime = Field(default_factory=datetime.utcnow())
    resolved: bool = False

    class Config:
        populate_by_name = True

class ErrorLogResponse(ErrorLogDB):
    pass

class AdminStatsBase(BaseModel):
    period: str
    new_users: int
    active_sessions: int
    documents_processed: int
    ai_queries_made: int
    vision_queries_made: int
    revenue: float
    subscription_upgrades: int
    support_tickets: int

class AdminStatsCreate(AdminStatsBase):
    pass

class AdminStatsDB(AdminStatsBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    recorded_at: datetime = Field(default_factory=datetime.utcnow())

    class Config:
        populate_by_name = True

class AdminStatsResponse(AdminStatsDB):
    pass
