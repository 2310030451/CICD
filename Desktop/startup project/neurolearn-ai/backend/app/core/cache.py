import json
import redis.asyncio as redis
from typing import Optional, Any
from loguru import logger
from app.config import settings

class CacheManager:
    """Redis cache manager for caching frequently accessed data"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def get_client(self) -> redis.Redis:
        """Get or create Redis client"""
        if self.redis_client is None:
            self.redis_client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            client = await self.get_client()
            value = await client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        try:
            client = await self.get_client()
            serialized = json.dumps(value)
            await client.set(key, serialized, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            client = await self.get_client()
            await client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern"""
        try:
            client = await self.get_client()
            keys = await client.keys(pattern)
            if keys:
                await client.delete(*keys)
            return len(keys)
        except Exception as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")
            return 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            client = await self.get_client()
            return await client.exists(key) > 0
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key"""
        try:
            client = await self.get_client()
            return await client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Cache expire error for key {key}: {e}")
            return False
    
    async def get_or_set(self, key: str, fetch_func, expire: int = 3600) -> Any:
        """Get value from cache or fetch and set it"""
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value
        
        # Fetch the value
        value = await fetch_func()
        
        # Set in cache
        await self.set(key, value, expire)
        
        return value
    
    async def clear_all(self) -> bool:
        """Clear all cache entries"""
        try:
            client = await self.get_client()
            await client.flushdb()
            logger.info("Cache cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None

# Global cache manager instance
cache = CacheManager()

# Cache key generators
def user_cache_key(user_id: str) -> str:
    """Generate cache key for user data"""
    return f"user:{user_id}"

def digital_twin_cache_key(user_id: str) -> str:
    """Generate cache key for digital twin"""
    return f"digital_twin:{user_id}"

def recommendations_cache_key(user_id: str) -> str:
    """Generate cache key for recommendations"""
    return f"recommendations:{user_id}"

def predictions_cache_key(user_id: str) -> str:
    """Generate cache key for predictions"""
    return f"predictions:{user_id}"

def subscription_cache_key(user_id: str) -> str:
    """Generate cache key for subscription"""
    return f"subscription:{user_id}"

def analytics_cache_key(user_id: str, period: str) -> str:
    """Generate cache key for analytics"""
    return f"analytics:{user_id}:{period}"

def course_cache_key(course_id: str) -> str:
    """Generate cache key for course"""
    return f"course:{course_id}"

def batch_cache_key(batch_id: str) -> str:
    """Generate cache key for batch"""
    return f"batch:{batch_id}"
