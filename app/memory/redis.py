from functools import lru_cache
from typing import Any

import redis

from app.core.config import get_settings


@lru_cache
def get_redis() -> Any:
    settings = get_settings()

    return redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
