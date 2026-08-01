import json
from typing import Any

from app.memory.redis import get_redis
from app.state.state import AgentState

client = get_redis()


def save(user_id: str, session_id: str, state: AgentState, message: str) -> None:
    key = f"chat:{user_id}:{session_id}"

    client.rpush(key, json.dumps(message))


def get_history(user_id: str, session_id: str) -> list[Any]:
    key = f"chat:{user_id}:{session_id}"

    messages = client.lrange(key, 0, -1)

    return [json.loads(message) for message in messages]
