from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.auth.jwt import verify_token
from app.core.contextvars import request_context

security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    print(f"auth scheme {credentials.scheme}")
    print(f"Token {credentials.credentials[:10]}")
    user = verify_token(credentials.credentials)
    ctx = request_context.get()
    ctx.user_id = user.id

    return user

