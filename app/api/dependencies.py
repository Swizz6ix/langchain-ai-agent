from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt import verify_token
from app.auth.models import User
from app.core.contextvars import request_context

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    user = verify_token(credentials.credentials)
    ctx = request_context.get()
    ctx.user_id = user.id

    return user
