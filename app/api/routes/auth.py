from fastapi import APIRouter, HTTPException

from app.auth.models import LoginRequest, RegisterRequest, TokenRequest, User
from app.auth.service import authenticate, register

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenRequest)
async def login(request: LoginRequest) -> TokenRequest:

    try:
        return authenticate(request)

    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@router.post("/register", response_model=User)
async def register_user(request: RegisterRequest) -> User:
    try:
        return register(request)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
