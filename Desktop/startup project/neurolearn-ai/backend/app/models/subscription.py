from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SubscriptionPlan(str, Enum):
    FREE = "free"
    STUDENT_PRO = "student_pro"
    PREMIUM = "premium"
    INSTITUTION = "institution"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"

class SubscriptionBase(BaseModel):
    user_id: str
    plan: SubscriptionPlan
    status: SubscriptionStatus
    ai_credits_used: int = 0
    ai_credits_limit: int
    documents_used: int = 0
    documents_limit: int
    vision_ai_used: int = 0
    vision_ai_limit: int
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    plan: Optional[SubscriptionPlan] = None
    status: Optional[SubscriptionStatus] = None
    ai_credits_used: Optional[int] = None
    documents_used: Optional[int] = None
    vision_ai_used: Optional[int] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

class SubscriptionDB(SubscriptionBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False

    class Config:
        populate_by_name = True

class SubscriptionResponse(SubscriptionDB):
    pass

class InvoiceBase(BaseModel):
    user_id: str
    subscription_id: str
    amount: float
    currency: str = "usd"
    status: str
    stripe_invoice_id: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceDB(InvoiceBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None
    invoice_url: Optional[str] = None

    class Config:
        populate_by_name = True

class InvoiceResponse(InvoiceDB):
    pass

class CouponBase(BaseModel):
    code: str
    discount_percentage: float
    max_uses: Optional[int] = None
    used_count: int = 0
    valid_from: datetime
    valid_until: datetime
    is_active: bool = True

class CouponCreate(CouponBase):
    pass

class CouponDB(CouponBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class CouponResponse(CouponDB):
    pass

class PaymentHistoryBase(BaseModel):
    user_id: str
    amount: float
    currency: str = "usd"
    payment_method: str
    status: str
    description: Optional[str] = None

class PaymentHistoryCreate(PaymentHistoryBase):
    pass

class PaymentHistoryDB(PaymentHistoryBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    stripe_payment_intent_id: Optional[str] = None

    class Config:
        populate_by_name = True

class PaymentHistoryResponse(PaymentHistoryDB):
    pass
