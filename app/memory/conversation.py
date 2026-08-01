import redis
import json

from app.memory.redis import get_redis

client = get_redis()

def save(user_id, session_id, state, message):
    key = f"chat:{user_id}:{session_id}"

    client.rpush(key, json.dumps(message))

def get_history(user_id, session_id):
    key = f"chat:{user_id}:{session_id}"

    messages = client.lrange(key, 0, -1)

    return [json.loads(message) for message in messages]