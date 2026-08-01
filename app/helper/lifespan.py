from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.memory.redis import get_redis


@asynccontextmanager
async def get_lifespan(app: FastAPI):
    redis = get_redis()

    app.state.redis = redis
    yield
    app.state.redis.close()