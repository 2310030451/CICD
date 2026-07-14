from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from loguru import logger
import stripe
from app.config import settings
from app.core.database import get_database
from app.models.subscription import (
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse,
    InvoiceResponse, CouponCreate, CouponResponse, PaymentHistoryResponse
)
from datetime import datetime
from typing import List

router = APIRouter()
security = HTTPBearer()

# Subscription Plan Limits
PLAN_LIMITS = {
    "free": {
        "ai_credits_limit": 100,
        "documents_limit": 10,
        "vision_ai_limit": 20
    },
    "student_pro": {
        "ai_credits_limit": 1000,
        "documents_limit": 100,
        "vision_ai_limit": 200
    },
    "premium": {
        "ai_credits_limit": 5000,
        "documents_limit": 500,
        "vision_ai_limit": 1000
    },
    "institution": {
        "ai_credits_limit": 20000,
        "documents_limit": 2000,
        "vision_ai_limit": 5000
    },
    "enterprise": {
        "ai_credits_limit": 100000,
        "documents_limit": 10000,
        "vision_ai_limit": 25000
    }
}

@router.get("/", response_model=List[SubscriptionResponse])
async def get_subscriptions(token: str = Depends(security)):
    """Get all subscriptions (admin only)"""
    db = await get_database()
    subscriptions = await db.subscriptions.find().to_list(100)
    return subscriptions

@router.get("/my-subscription", response_model=SubscriptionResponse)
async def get_my_subscription(token: str = Depends(security)):
    """Get current user's subscription"""
    db = await get_database()
    # Extract user_id from token (simplified - in production, decode JWT)
    user_id = token.credentials  # This should be the actual user_id from JWT
    
    subscription = await db.subscriptions.find_one({"user_id": user_id})
    if not subscription:
        # Create free subscription for new users
        limits = PLAN_LIMITS["free"]
        subscription_data = {
            "user_id": user_id,
            "plan": "free",
            "status": "active",
            "ai_credits_used": 0,
            "ai_credits_limit": limits["ai_credits_limit"],
            "documents_used": 0,
            "documents_limit": limits["documents_limit"],
            "vision_ai_used": 0,
            "vision_ai_limit": limits["vision_ai_limit"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await db.subscriptions.insert_one(subscription_data)
        subscription = subscription_data
    
    return subscription

@router.post("/create-checkout-session")
async def create_checkout_session(plan: str, token: str = Depends(security)):
    """Create Stripe checkout session for subscription"""
    if plan not in PLAN_LIMITS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    db = await get_database()
    user_id = token.credentials
    
    # Get or create Stripe customer
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.get("stripe_customer_id"):
        customer = stripe.Customer.create(email=user.get("email"))
        await db.users.update_one(
            {"_id": user_id},
            {"": {"stripe_customer_id": customer.id}}
        )
        stripe_customer_id = customer.id
    else:
        stripe_customer_id = user["stripe_customer_id"]
    
    # Create checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=stripe_customer_id,
            line_items=[
                {
                    "price": settings.stripe_price_ids[plan],
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{settings.frontend_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_url}/subscription/cancel",
            metadata={"user_id": user_id, "plan": plan}
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        logger.error(f"Failed to create checkout session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")

@router.post("/cancel")
async def cancel_subscription(token: str = Depends(security)):
    """Cancel user's subscription"""
    db = await get_database()
    user_id = token.credentials
    
    subscription = await db.subscriptions.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.get("stripe_subscription_id"):
        try:
            stripe.Subscription.delete(subscription["stripe_subscription_id"])
        except Exception as e:
            logger.error(f"Failed to cancel Stripe subscription: {e}")
    
    await db.subscriptions.update_one(
        {"user_id": user_id},
        {"": {"status": "cancelled", "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Subscription cancelled successfully"}

@router.get("/invoices", response_model=List[InvoiceResponse])
async def get_invoices(token: str = Depends(security)):
    """Get user's invoices"""
    db = await get_database()
    user_id = token.credentials
    
    invoices = await db.invoices.find({"user_id": user_id}).to_list(50)
    return invoices

@router.get("/payment-history", response_model=List[PaymentHistoryResponse])
async def get_payment_history(token: str = Depends(security)):
    """Get user's payment history"""
    db = await get_database()
    user_id = token.credentials
    
    payments = await db.payment_history.find({"user_id": user_id}).to_list(50)
    return payments

@router.post("/coupons", response_model=CouponResponse)
async def create_coupon(coupon: CouponCreate, token: str = Depends(security)):
    """Create a coupon (admin only)"""
    db = await get_database()
    
    coupon_data = coupon.dict()
    coupon_data["created_at"] = datetime.utcnow()
    
    result = await db.coupons.insert_one(coupon_data)
    coupon_data["id"] = str(result.inserted_id)
    
    return coupon_data

@router.post("/validate-coupon")
async def validate_coupon(code: str, token: str = Depends(security)):
    """Validate a coupon code"""
    db = await get_database()
    
    coupon = await db.coupons.find_one({"code": code, "is_active": True})
    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon code")
    
    now = datetime.utcnow()
    if now < coupon["valid_from"] or now > coupon["valid_until"]:
        raise HTTPException(status_code=400, detail="Coupon expired")
    
    if coupon["max_uses"] and coupon["used_count"] >= coupon["max_uses"]:
        raise HTTPException(status_code=400, detail="Coupon usage limit reached")
    
    return {
        "valid": True,
        "discount_percentage": coupon["discount_percentage"]
    }

@router.get("/usage")
async def get_usage(token: str = Depends(security)):
    """Get current usage statistics"""
    db = await get_database()
    user_id = token.credentials
    
    subscription = await db.subscriptions.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return {
        "ai_credits": {
            "used": subscription["ai_credits_used"],
            "limit": subscription["ai_credits_limit"],
            "remaining": subscription["ai_credits_limit"] - subscription["ai_credits_used"]
        },
        "documents": {
            "used": subscription["documents_used"],
            "limit": subscription["documents_limit"],
            "remaining": subscription["documents_limit"] - subscription["documents_used"]
        },
        "vision_ai": {
            "used": subscription["vision_ai_used"],
            "limit": subscription["vision_ai_limit"],
            "remaining": subscription["vision_ai_limit"] - subscription["vision_ai_used"]
        }
    }
