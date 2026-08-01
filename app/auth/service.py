import uuid
from app.auth.jwt import create_access_token
from app.auth.models import (LoginRequest, RegisterRequest, TokenRequest, User)
from app.auth.password import (hash_password, verify_password)

fake_db: dict[str, dict] = {}

def register(request: RegisterRequest) -> User:
    if request.email in fake_db:
        raise ValueError("Email already exist")

    user = User(
        id = str(uuid.uuid4()),
        email = request.email,
        role = "user"
    )

    print(f"User {user}")

    fake_db[request.email] = {
        "user": user,
        "password": hash_password(request.password),
    }

    print(f"db >>> {fake_db}")

    return user


def authenticate(request: LoginRequest) -> TokenRequest:
    record = fake_db.get(request.email)

    if record is None:
        raise ValueError("Invalid credentials")
    
    if not verify_password(request.password, record["password"]):
        raise ValueError("Invalid credentials")

    token = create_access_token(record["user"])

    print(f"token {token}")

    return TokenRequest(access_token = token)

print(f"db {fake_db}")