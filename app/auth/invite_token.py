from datetime import datetime, timedelta, timezone
from uuid import UUID
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import get_settings
from app.services.role import Role

settings = get_settings()

def create_invite_token(
    invite_id: UUID,
    email: str,
    tenant_id: UUID,
    role: Role,
    expires_delta: timedelta = timedelta(days=7),
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": invite_id,
        "email": email,
        "tenant_id": tenant_id,
        "role": role,
        "type": "invite",
        "iat": now,
        "exp": now + expires_delta,
        "iss": settings.jwt_iss,
        "aud": "invite",
    }

    return jwt.encode(
        payload,
        settings.invite_secret,
        algorithm = settings.jwt_algorithm,
    )

def verify_invite_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, 
            settings.invite_secret,
            algorithms = [settings.jwt_algorithm],
            issuer = settings.jwt_iss,
            audience = "invite",
        )

        if payload["type"] != "invite":
            raise ValueError("Invalid token type")

        return payload
    
    except ExpiredSignatureError:
        raise ValueError("Invite link has expired")
    
    except JWTError:
        raise ValueError("Invalid invite token")