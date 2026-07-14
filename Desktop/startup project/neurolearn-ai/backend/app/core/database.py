from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger
from app.config import settings


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def init_db():
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
        db.database = db.client[settings.mongodb_database]
        
        await db.client.admin.command('ping')
        logger.info(f"Connected to MongoDB at {settings.mongodb_uri}")
        
        await create_indexes()
    except Exception as e:
        logger.warning(f"Failed to connect to MongoDB: {e}. Backend will start with degraded functionality.")
        logger.warning("MongoDB-dependent features will be unavailable until database connection is established.")
        db.client = None
        db.database = None


async def close_db():
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")


async def create_indexes():
    try:
        await db.database.users.create_index("firebase_uid", unique=True)
        await db.database.users.create_index("email", unique=True)
        
        await db.database.profiles.create_index("user_id", unique=True)
        
        await db.database.content.create_index("user_id")
        await db.database.content.create_index("file_hash", unique=True)
        await db.database.content.create_index([("user_id", 1), ("created_at", -1)])
        
        await db.database.sessions.create_index("user_id")
        await db.database.sessions.create_index([("user_id", 1), ("created_at", -1)])
        
        await db.database.quizzes.create_index("user_id")
        await db.database.quizzes.create_index([("user_id", 1), ("created_at", -1)])
        
        await db.database.analytics.create_index("user_id")
        await db.database.analytics.create_index([("user_id", 1), ("date", -1)])
        
        await db.database.documents.create_index("user_id")
        await db.database.documents.create_index("file_hash", unique=True)
        await db.database.documents.create_index([("user_id", 1), ("created_at", -1)])
        await db.database.documents.create_index([("user_id", 1), ("status", 1)])
        
        await db.database.conversations.create_index("user_id")
        await db.database.conversations.create_index([("user_id", 1), ("updated_at", -1)])
        
        await db.database.vision_images.create_index("user_id")
        await db.database.vision_images.create_index("file_hash", unique=True)
        await db.database.vision_images.create_index([("user_id", 1), ("created_at", -1)])
        await db.database.vision_images.create_index([("user_id", 1), ("status", 1)])
        await db.database.vision_images.create_index([("user_id", 1), ("image_type", 1)])
        
        await db.database.learning_events.create_index("user_id")
        await db.database.learning_events.create_index([("user_id", 1), ("timestamp", -1)])
        await db.database.learning_events.create_index([("user_id", 1), ("event_type", 1)])
        
        await db.database.predictions.create_index("user_id")
        await db.database.predictions.create_index([("user_id", 1), ("created_at", -1)])
        
        await db.database.digital_twins.create_index("user_id", unique=True)
        await db.database.digital_twins.create_index([("user_id", 1), ("last_updated", -1)])
        
        await db.database.study_plans.create_index("user_id")
        await db.database.study_plans.create_index([("user_id", 1), ("created_at", -1)])
        await db.database.study_plans.create_index([("user_id", 1), ("status", 1)])
        
        await db.database.revision_plans.create_index("user_id")
        await db.database.revision_plans.create_index([("user_id", 1), ("created_at", -1)])
        await db.database.revision_plans.create_index([("user_id", 1), ("status", 1)])
        
        await db.database.agent_memory.create_index("user_id")
        await db.database.agent_memory.create_index([("user_id", 1), ("agent_name", 1)])
        await db.database.agent_memory.create_index([("user_id", 1), ("timestamp", -1)])
        
        await db.database.recommendations.create_index("user_id")
        await db.database.recommendations.create_index([("user_id", 1), ("created_at", -1)])
        
        # Subscription and payment indexes
        await db.database.subscriptions.create_index("user_id")
        await db.database.subscriptions.create_index([("user_id", 1), ("status", 1)])
        await db.database.subscriptions.create_index("stripe_subscription_id", unique=True)
        
        await db.database.invoices.create_index("user_id")
        await db.database.invoices.create_index("subscription_id")
        await db.database.invoices.create_index("stripe_invoice_id", unique=True)
        
        await db.database.coupons.create_index("code", unique=True)
        await db.database.coupons.create_index([("is_active", 1)])
        
        await db.database.payment_history.create_index("user_id")
        await db.database.payment_history.create_index("subscription_id")
        
        # Admin and system indexes
        await db.database.system_metrics.create_index([("timestamp", -1)])
        
        await db.database.audit_logs.create_index("user_id")
        await db.database.audit_logs.create_index([("user_id", 1), ("timestamp", -1)])
        await db.database.audit_logs.create_index([("action", 1), ("timestamp", -1)])
        await db.database.audit_logs.create_index([("resource", 1), ("timestamp", -1)])
        
        await db.database.system_health.create_index([("timestamp", -1)])
        
        await db.database.error_logs.create_index([("timestamp", -1)])
        await db.database.error_logs.create_index([("is_resolved", 1)])
        
        # Teacher-related indexes
        await db.database.courses.create_index("teacher_id")
        await db.database.courses.create_index([("teacher_id", 1), ("status", 1)])
        
        await db.database.notes.create_index("teacher_id")
        await db.database.notes.create_index("course_id")
        
        await db.database.assignments.create_index("teacher_id")
        await db.database.assignments.create_index("course_id")
        
        await db.database.student_progress.create_index("student_id")
        await db.database.student_progress.create_index("course_id")
        
        await db.database.attendance_records.create_index("student_id")
        await db.database.attendance_records.create_index("course_id")
        await db.database.attendance_records.create_index([("student_id", 1), ("date", -1)])
        
        await db.database.batches.create_index("teacher_id")
        await db.database.batches.create_index([("teacher_id", 1), ("status", 1)])
        
        # Parent-related indexes
        await db.database.parent_child_relations.create_index("parent_id")
        await db.database.parent_child_relations.create_index("child_id")
        await db.database.parent_child_relations.create_index([("parent_id", 1), ("child_id", 1)], unique=True)
        
        await db.database.student_progress_reports.create_index("parent_id")
        await db.database.student_progress_reports.create_index("child_id")
        await db.database.student_progress_reports.create_index([("child_id", 1), ("generated_at", -1)])
        
        await db.database.parent_notifications.create_index("parent_id")
        await db.database.parent_notifications.create_index("child_id")
        await db.database.parent_notifications.create_index([("parent_id", 1), ("is_read", 1)])
        
        await db.database.revision_calendar.create_index("parent_id")
        await db.database.revision_calendar.create_index("child_id")
        await db.database.revision_calendar.create_index([("child_id", 1), ("scheduled_date", 1)])
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")


async def get_database():
    return db.database
