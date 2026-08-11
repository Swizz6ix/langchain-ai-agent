import secrets
import hashlib

def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_token(token:str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()