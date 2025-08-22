"""
Redis connection and utilities for caching, sessions, and queues.
"""

import json
from typing import Any, Optional, Union
import redis.asyncio as redis
from loguru import logger
from app.core.config import settings
import time


class RedisClient:
    """Redis client for caching, sessions, and queues."""
    
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        try:
            self.client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
            )
            
            # Test connection
            await self.client.ping()
            logger.info("Connected to Redis successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis."""
        try:
            if self.client:
                return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis get error: {str(e)}")
        return None
    
    async def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiration."""
        try:
            if self.client:
                await self.client.set(key, value, ex=expire)
                return True
        except Exception as e:
            logger.error(f"Redis set error: {str(e)}")
        return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        try:
            if self.client:
                await self.client.delete(key)
                return True
        except Exception as e:
            logger.error(f"Redis delete error: {str(e)}")
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        try:
            if self.client:
                return bool(await self.client.exists(key))
        except Exception as e:
            logger.error(f"Redis exists error: {str(e)}")
        return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for key."""
        try:
            if self.client:
                return bool(await self.client.expire(key, seconds))
        except Exception as e:
            logger.error(f"Redis expire error: {str(e)}")
        return False
    
    async def incr(self, key: str) -> Optional[int]:
        """Increment value in Redis."""
        try:
            if self.client:
                return await self.client.incr(key)
        except Exception as e:
            logger.error(f"Redis incr error: {str(e)}")
        return None
    
    async def hget(self, name: str, key: str) -> Optional[str]:
        """Get hash field value."""
        try:
            if self.client:
                return await self.client.hget(name, key)
        except Exception as e:
            logger.error(f"Redis hget error: {str(e)}")
        return None
    
    async def hset(self, name: str, key: str, value: str) -> bool:
        """Set hash field value."""
        try:
            if self.client:
                await self.client.hset(name, key, value)
                return True
        except Exception as e:
            logger.error(f"Redis hset error: {str(e)}")
        return False
    
    async def hgetall(self, name: str) -> dict:
        """Get all hash fields."""
        try:
            if self.client:
                return await self.client.hgetall(name)
        except Exception as e:
            logger.error(f"Redis hgetall error: {str(e)}")
        return {}
    
    async def lpush(self, name: str, *values) -> Optional[int]:
        """Push values to list from left."""
        try:
            if self.client:
                return await self.client.lpush(name, *values)
        except Exception as e:
            logger.error(f"Redis lpush error: {str(e)}")
        return None
    
    async def rpop(self, name: str) -> Optional[str]:
        """Pop value from list from right."""
        try:
            if self.client:
                return await self.client.rpop(name)
        except Exception as e:
            logger.error(f"Redis rpop error: {str(e)}")
        return None
    
    async def llen(self, name: str) -> int:
        """Get list length."""
        try:
            if self.client:
                return await self.client.llen(name)
        except Exception as e:
            logger.error(f"Redis llen error: {str(e)}")
        return 0
    
    async def sadd(self, name: str, *values) -> Optional[int]:
        """Add values to set."""
        try:
            if self.client:
                return await self.client.sadd(name, *values)
        except Exception as e:
            logger.error(f"Redis sadd error: {str(e)}")
        return None
    
    async def srem(self, name: str, *values) -> Optional[int]:
        """Remove values from set."""
        try:
            if self.client:
                return await self.client.srem(name, *values)
        except Exception as e:
            logger.error(f"Redis srem error: {str(e)}")
        return None
    
    async def smembers(self, name: str) -> set:
        """Get all set members."""
        try:
            if self.client:
                return await self.client.smembers(name)
        except Exception as e:
            logger.error(f"Redis smembers error: {str(e)}")
        return set()
    
    async def zadd(self, name: str, mapping: dict) -> Optional[int]:
        """Add values to sorted set."""
        try:
            if self.client:
                return await self.client.zadd(name, mapping)
        except Exception as e:
            logger.error(f"Redis zadd error: {str(e)}")
        return None
    
    async def zrange(self, name: str, start: int, end: int, desc: bool = False) -> list:
        """Get range from sorted set."""
        try:
            if self.client:
                return await self.client.zrange(name, start, end, desc=desc)
        except Exception as e:
            logger.error(f"Redis zrange error: {str(e)}")
        return []
    
    async def pipeline(self):
        """Get Redis pipeline for batch operations."""
        if self.client:
            return self.client.pipeline()
        return None


# Global Redis client instance
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """Dependency to get Redis client."""
    return redis_client


# Cache utilities
class Cache:
    """Cache utilities using Redis."""
    
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set cached value."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self.redis.set(key, str(value), expire)
    
    async def delete(self, key: str) -> bool:
        """Delete cached value."""
        return await self.redis.delete(key)
    
    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern."""
        try:
            if self.redis.client:
                keys = await self.redis.client.keys(pattern)
                if keys:
                    await self.redis.client.delete(*keys)
                return True
        except Exception as e:
            logger.error(f"Cache clear pattern error: {str(e)}")
        return False


# Session utilities
class SessionManager:
    """Session management using Redis."""
    
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client
        self.session_prefix = "session:"
        self.default_expire = 3600  # 1 hour
    
    async def create_session(self, user_id: str, data: dict = None) -> str:
        """Create new session."""
        session_id = f"{self.session_prefix}{user_id}:{int(time.time())}"
        session_data = {
            "user_id": user_id,
            "created_at": int(time.time()),
            "data": data or {}
        }
        await self.redis.set(session_id, json.dumps(session_data), self.default_expire)
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data."""
        data = await self.redis.get(session_id)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None
    
    async def update_session(self, session_id: str, data: dict) -> bool:
        """Update session data."""
        session = await self.get_session(session_id)
        if session:
            session["data"].update(data)
            return await self.redis.set(session_id, json.dumps(session), self.default_expire)
        return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session."""
        return await self.redis.delete(session_id)
    
    async def clean_expired_sessions(self) -> int:
        """Clean expired sessions (Redis handles this automatically)."""
        return 0


# Queue utilities
class Queue:
    """Simple queue implementation using Redis lists."""
    
    def __init__(self, redis_client: RedisClient, queue_name: str):
        self.redis = redis_client
        self.queue_name = f"queue:{queue_name}"
    
    async def enqueue(self, data: Any) -> bool:
        """Add item to queue."""
        try:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            await self.redis.lpush(self.queue_name, str(data))
            return True
        except Exception as e:
            logger.error(f"Queue enqueue error: {str(e)}")
            return False
    
    async def dequeue(self) -> Optional[Any]:
        """Remove and return item from queue."""
        try:
            data = await self.redis.rpop(self.queue_name)
            if data:
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return data
        except Exception as e:
            logger.error(f"Queue dequeue error: {str(e)}")
        return None
    
    async def size(self) -> int:
        """Get queue size."""
        return await self.redis.llen(self.queue_name)
    
    async def clear(self) -> bool:
        """Clear queue."""
        return await self.redis.delete(self.queue_name)
