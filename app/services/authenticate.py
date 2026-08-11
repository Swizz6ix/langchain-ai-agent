from typing import Any
from datetime import datetime, timezone, timedelta

from app.auth.jwt import create_access_token
from app.models.authenticate_request import LoginRequest
from app.models.token_response import TokenResponse
from app.auth.password import verify_password
from app.services.base_service import BaseService
from app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.helper.refresh_token import create_refresh_token, hash_token
from app.models.refresh_token_request import RefreshTokenRequest
from app.domain.exceptions import InvalidCredentialsError
from app.models.refresh_token import RefreshToken

class AuthenticationService(BaseService):
    def __init__(self, uow):
        super().__init__(uow)

    async def authenticate(self, request: LoginRequest) -> TokenResponse:
        user = await self.uow.users.get_by_email(request.email)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(request.password, user.hash_password):
            raise InvalidCredentialsError()

        access_token = create_access_token(user)
        refresh_token = create_refresh_token()

        expires_at = datetime.now(timezone.utc) + timedelta(days = 7)

        refresh_tokn = RefreshToken(
            user_id = user.id,
            token_hash = hash_token(refresh_token),
            expires_at = expires_at,
        )

        await self.uow.refresh.create(refresh_tokn)

        return TokenResponse(
            access_token = access_token,
            refresh_token = refresh_token,
        )

    async def refresh_access_token(
        self,
        request: RefreshTokenRequest,
    ) -> TokenResponse:
        token_hash = hash_token(request.refresh_token)
    
        refresh = await self.uow.refresh.get_by_hash(token_hash)
    
        if refresh is None:
            raise ValueError("Invalid refresh token")
    
        if refresh.revoked:
            raise ValueError("Refresh token revoked")
    
        if refresh.expires_at < datetime.now(timezone.utc):
            await self.uow.refresh.delete(refresh)
            await self.uow.commit()
            
            raise ValueError("Refresh token expired")
    
        user = await self.uow.users.get_by_id(refresh.user_id)
    
        access_token = create_access_token(user)
    
        return TokenResponse(
            access_token=access_token
        )