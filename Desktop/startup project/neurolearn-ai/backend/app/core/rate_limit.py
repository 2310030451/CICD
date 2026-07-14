from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time
from typing import Dict
from collections import defaultdict
import redis.asyncio as redis
from app.config import settings

class RateLimiter:
    """Simple in-memory rate limiter (for production, use Redis-based limiter)"""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """Check if request is allowed based on rate limit"""
        now = time.time()
        
        # Remove old requests outside the window
        self.requests[key] = [t for t in self.requests[key] if now - t < window]
        
        # Check if limit exceeded
        if len(self.requests[key]) >= limit:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True

class RedisRateLimiter:
    """Redis-based rate limiter for production use"""
    
    def __init__(self):
        self.redis_client = None
    
    async def get_client(self):
        """Get Redis client"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """Check if request is allowed using Redis"""
        try:
            client = await self.get_client()
            
            # Use Redis INCR and EXPIRE for rate limiting
            current = await client.incr(key)
            
            if current == 1:
                # Set expiration on first request
                await client.expire(key, window)
            
            return current <= limit
        
        except Exception as e:
            logger.error(f"Redis rate limiter error: {e}")
            # Fallback to allowing request if Redis fails
            return True

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce rate limiting on API endpoints"""
    
    def __init__(self, app, use_redis: bool = False):
        super().__init__(app)
        self.use_redis = use_redis
        self.limiter = RedisRateLimiter() if use_redis else RateLimiter()
        
        # Rate limits per endpoint type
        self.limits = {
            "default": {"limit": 100, "window": 60},  # 100 requests per minute
            "auth": {"limit": 10, "window": 60},  # 10 auth requests per minute
            "upload": {"limit": 20, "window": 60},  # 20 uploads per minute
            "ai": {"limit": 30, "window": 60},  # 30 AI requests per minute
        }
    
    def get_rate_limit_key(self, request: Request) -> str:
        """Generate rate limit key based on IP and endpoint"""
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        
        # Different limits for different endpoint types
        if "/auth" in path:
            limit_type = "auth"
        elif "/upload" in path or "/documents" in path:
            limit_type = "upload"
        elif "/ai" in path or "/chat" in path or "/agents" in path:
            limit_type = "ai"
        else:
            limit_type = "default"
        
        return f"rate_limit:{limit_type}:{client_ip}"
    
    def get_limit_for_type(self, limit_type: str) -> dict:
        """Get rate limit configuration for endpoint type"""
        return self.limits.get(limit_type, self.limits["default"])
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting"""
        # Skip rate limiting for health checks and webhooks
        if "/health" in request.url.path or "/webhook" in request.url.path:
            return await call_next(request)
        
        # Get rate limit key
        key = self.get_rate_limit_key(request)
        
        # Determine limit type
        path = request.url.path
        if "/auth" in path:
            limit_type = "auth"
        elif "/upload" in path or "/documents" in path:
            limit_type = "upload"
        elif "/ai" in path or "/chat" in path or "/agents" in path:
            limit_type = "ai"
        else:
            limit_type = "default"
        
        limit_config = self.get_limit_for_type(limit_type)
        
        # Check if request is allowed
        if self.use_redis:
            allowed = await self.limiter.is_allowed(key, limit_config["limit"], limit_config["window"])
        else:
            allowed = self.limiter.is_allowed(key, limit_config["limit"], limit_config["window"])
        
        if not allowed:
            logger.warning(f"Rate limit exceeded for {key}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": limit_config["limit"],
                    "window": limit_config["window"],
                    "retry_after": limit_config["window"]
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit_config["limit"])
        response.headers["X-RateLimit-Window"] = str(limit_config["window"])
        response.headers["X-RateLimit-Remaining"] = str(limit_config["limit"] - 1)
        
        return response

def get_rate_limit_middleware(use_redis: bool = False):
    """Get rate limiting middleware"""
    return RateLimitMiddleware(use_redis=use_redis)
