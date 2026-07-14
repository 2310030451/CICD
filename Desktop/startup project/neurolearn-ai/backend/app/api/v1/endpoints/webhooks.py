from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from loguru import logger
import stripe
from app.config import settings
from app.core.database import get_database
from app.models.subscription import SubscriptionDB, InvoiceDB, PaymentHistoryDB
from datetime import datetime

router = APIRouter()

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    db = await get_database()
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_completed(session, db)
    
    elif event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        await handle_subscription_created(subscription, db)
    
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        await handle_subscription_updated(subscription, db)
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        await handle_subscription_deleted(subscription, db)
    
    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        await handle_invoice_payment_succeeded(invoice, db)
    
    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        await handle_invoice_payment_failed(invoice, db)
    
    return JSONResponse(status_code=200, content={"status": "success"})

async def handle_checkout_completed(session, db):
    """Handle successful checkout session"""
    user_id = session.get("metadata", {}).get("user_id")
    if not user_id:
        logger.error("No user_id in session metadata")
        return
    
    logger.info(f"Checkout completed for user {user_id}")
    
async def handle_subscription_created(subscription, db):
    """Handle subscription creation"""
    customer_id = subscription["customer"]
    subscription_id = subscription["id"]
    
    user = await db.users.find_one({"stripe_customer_id": customer_id})
    if not user:
        logger.error(f"No user found for customer {customer_id}")
        return
    
    plan = subscription["items"]["data"][0]["price"]["lookup_key"]
    status = subscription["status"]
    
    await db.subscriptions.update_one(
        {"user_id": str(user["_id"])},
        {
            "": {
                "stripe_subscription_id": subscription_id,
                "status": status,
                "current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
                "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    logger.info(f"Subscription created for user {user['_id']}")

async def handle_subscription_updated(subscription, db):
    """Handle subscription update"""
    customer_id = subscription["customer"]
    subscription_id = subscription["id"]
    
    user = await db.users.find_one({"stripe_customer_id": customer_id})
    if not user:
        logger.error(f"No user found for customer {customer_id}")
        return
    
    status = subscription["status"]
    
    await db.subscriptions.update_one(
        {"user_id": str(user["_id"])},
        {
            "": {
                "status": status,
                "current_period_start": datetime.fromtimestamp(subscription["current_period_start"]),
                "current_period_end": datetime.fromtimestamp(subscription["current_period_end"]),
                "cancel_at_period_end": subscription.get("cancel_at_period_end", False),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    logger.info(f"Subscription updated for user {user['_id']}")

async def handle_subscription_deleted(subscription, db):
    """Handle subscription cancellation"""
    customer_id = subscription["customer"]
    
    user = await db.users.find_one({"stripe_customer_id": customer_id})
    if not user:
        logger.error(f"No user found for customer {customer_id}")
        return
    
    await db.subscriptions.update_one(
        {"user_id": str(user["_id"])},
        {
            "": {
                "status": "cancelled",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    logger.info(f"Subscription cancelled for user {user['_id']}")

async def handle_invoice_payment_succeeded(invoice, db):
    """Handle successful invoice payment"""
    customer_id = invoice["customer"]
    subscription_id = invoice["subscription"]
    
    user = await db.users.find_one({"stripe_customer_id": customer_id})
    if not user:
        logger.error(f"No user found for customer {customer_id}")
        return
    
    # Create invoice record
    invoice_data = {
        "user_id": str(user["_id"]),
        "subscription_id": subscription_id,
        "amount": invoice["amount_paid"] / 100,
        "currency": invoice["currency"],
        "status": "paid",
        "stripe_invoice_id": invoice["id"],
        "created_at": datetime.utcnow(),
        "paid_at": datetime.fromtimestamp(invoice["status_transitions"]["paid_at"])
    }
    
    await db.invoices.insert_one(invoice_data)
    
    # Create payment history record
    payment_data = {
        "user_id": str(user["_id"]),
        "amount": invoice["amount_paid"] / 100,
        "currency": invoice["currency"],
        "payment_method": "stripe",
        "status": "succeeded",
        "description": f"Subscription payment",
        "created_at": datetime.utcnow(),
        "stripe_payment_intent_id": invoice.get("payment_intent")
    }
    
    await db.payment_history.insert_one(payment_data)
    
    logger.info(f"Payment succeeded for user {user['_id']}")

async def handle_invoice_payment_failed(invoice, db):
    """Handle failed invoice payment"""
    customer_id = invoice["customer"]
    
    user = await db.users.find_one({"stripe_customer_id": customer_id})
    if not user:
        logger.error(f"No user found for customer {customer_id}")
        return
    
    # Create payment history record for failed payment
    payment_data = {
        "user_id": str(user["_id"]),
        "amount": invoice["amount_due"] / 100,
        "currency": invoice["currency"],
        "payment_method": "stripe",
        "status": "failed",
        "description": f"Subscription payment failed",
        "created_at": datetime.utcnow()
    }
    
    await db.payment_history.insert_one(payment_data)
    
    logger.warning(f"Payment failed for user {user['_id']}")
