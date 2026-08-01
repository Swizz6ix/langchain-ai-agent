from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from app.memory.redis import get_redis


@asynccontextmanager
async def get_lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    redis = get_redis()

    app.state.redis = redis
    yield
    app.state.redis.close()
