import uuid
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt

from app.auth.models import User
from app.core.config import get_settings

settings = get_settings()


def create_access_token(user: User) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "iat": datetime.now(UTC),
        "exp": expire,
        "iss": settings.jwt_iss,
        "aud": settings.jwt_aud,
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def verify_token(token: str) -> User:

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_iss,
            audience=settings.jwt_aud,
        )

        return User(
            id=payload["sub"],
            email=payload["email"],
            role=payload["role"],
        )

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
