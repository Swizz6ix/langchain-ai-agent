from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.register_request import  RegisterRequest
from app.models.users import User
from app.auth.password import hash_password
from app.services.base_service import BaseService
from app.repositories.user_repository import UserRepository


class RegisterService(BaseService):

    async def register(self, request: RegisterRequest, db: AsyncSession) -> User:
        existing_email = await self.uow.users.get_by_email(
            db,
            request.email
        )
        
        if existing_email:
            raise ValueError("Email already exist")

        user = User(
            email = request.email, 
            hash_password = hash_password(request.password),
            role="user",
            tenant_id = "default"
        )

        await self.uow.users.create(user)

        return user
