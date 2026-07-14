from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.config import settings
from app.core.database import init_db, close_db
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.core.security import SecurityHeadersMiddleware, CSRFProtectionMiddleware
from app.core.rate_limit import RateLimitMiddleware


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting NeuroLearn AI backend...")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down NeuroLearn AI backend...")
    await close_db()
    logger.info("Database connection closed")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A multimodal AI-powered personalized learning platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Add CSRF protection middleware (disabled in development)
if settings.environment != "development":
    app.add_middleware(CSRFProtectionMiddleware, secret_key=settings.jwt_secret_key)

# Add rate limiting middleware (use Redis in production)
app.add_middleware(RateLimitMiddleware, use_redis=settings.environment != "development")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/")
async def root():
    return {
        "message": "Welcome to NeuroLearn AI API",
        "version": settings.app_version,
        "docs": "/api/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers,
    )
