import pytest
from app.core.cache import cache_manager
from app.config import settings


class TestCacheManager:
    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        """Test basic cache set and get operations"""
        await cache_manager.set("test_key", "test_value", ttl=60)
        value = await cache_manager.get("test_key")
        assert value == "test_value"
        
    @pytest.mark.asyncio
    async def test_cache_delete(self):
        """Test cache deletion"""
        await cache_manager.set("test_key_delete", "test_value", ttl=60)
        await cache_manager.delete("test_key_delete")
        value = await cache_manager.get("test_key_delete")
        assert value is None
        
    @pytest.mark.asyncio
    async def test_cache_pattern_delete(self):
        """Test pattern-based deletion"""
        await cache_manager.set("user:1:data", "value1", ttl=60)
        await cache_manager.set("user:2:data", "value2", ttl=60)
        await cache_manager.set("user:1:profile", "value3", ttl=60)
        
        await cache_manager.delete_pattern("user:1:*")
        
        value1 = await cache_manager.get("user:1:data")
        value2 = await cache_manager.get("user:2:data")
        value3 = await cache_manager.get("user:1:profile")
        
        assert value1 is None
        assert value2 == "value2"
        assert value3 is None
        
    @pytest.mark.asyncio
    async def test_cache_key_generators(self):
        """Test cache key generation"""
        user_key = cache_manager.get_user_cache_key("user123")
        assert "user" in user_key
        assert "user123" in user_key
        
        digital_twin_key = cache_manager.get_digital_twin_cache_key("user123")
        assert "digital_twin" in digital_twin_key
        assert "user123" in digital_twin_key


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
