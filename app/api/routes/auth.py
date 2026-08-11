from fastapi import APIRouter, Depends, HTTPException, status

from app.models.authenticate_request import LoginRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.models.register_request import RegisterRequest
from app.models.users import User
from app.services.register import RegisterService
from app.services.authenticate import AuthenticationService
from app.models.refresh_token_request import RefreshTokenRequest
from app.api.dependencies import get_auth_service, get_reg_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(request: LoginRequest, service: AuthenticationService = Depends(get_auth_service)):
    return await service.authenticate(request)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(request: RefreshTokenRequest, service: AuthenticationService = Depends(get_auth_service)):
    return await service.refresh_access_token(request)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: RegisterRequest, service: RegisterService = Depends(get_reg_service)):
    return await service.register(request)
