import redis.asyncio as redis
from app.core.config import settings

redis_client = None

async def get_redis() -> redis.Redis:
    """Создание и получение redis-клиента"""
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
    return redis_client
