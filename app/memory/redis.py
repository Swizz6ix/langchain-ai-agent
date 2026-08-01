import redis
from functools import lru_cache
from app.core.config import get_settings

@lru_cache
def get_redis():
    settings = get_settings()

    return redis.Redis(
        host = settings.redis_host,
        port = settings.redis_port,
        decode_responses = True
    )