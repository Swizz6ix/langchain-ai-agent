import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import JWTError, jwt
from app.auth.models import User
from app.core.config import get_settings

settings = get_settings()

def create_access_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes = settings.access_token_expire_minutes
    )

    print(f"exp {expire}")

    payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "iss": settings.jwt_iss,
        "aud": settings.jwt_aud,
        "jti": str(uuid.uuid4())
    }

    print(f"payload {payload}")

    print(f"encode {settings.jwt_secret}")
    print(f"encode {settings.jwt_algorithm}")

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm = settings.jwt_algorithm,
    )

def verify_token(token: str) -> User:
    print(f"decode {settings.jwt_secret}")
    print(f"decode {settings.jwt_algorithm}")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms = [settings.jwt_algorithm],
            issuer = settings.jwt_iss,
            audience = settings.jwt_aud,
        )

        print(f"verify {payload}")

        return User(
            id = payload["sub"],
            email = payload["email"],
            role = payload["role"],
        )

    except JWTError as err:
        raise HTTPException(
            status_code = 401,
            detail = f"Invalid token: {str(err)}"
        )