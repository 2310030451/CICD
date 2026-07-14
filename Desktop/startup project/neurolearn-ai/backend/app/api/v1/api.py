from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, content, sessions, quizzes, analytics, documents, chat, vision
from app.api.v1.endpoints import predictions, digital_twin, agents, recommendations, study_planner, revision_planner, voice, monitoring

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/ai", tags=["ai"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["digital-twin"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(study_planner.router, prefix="/study-planner", tags=["study-planner"])
api_router.include_router(revision_planner.router, prefix="/revision-planner", tags=["revision-planner"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
