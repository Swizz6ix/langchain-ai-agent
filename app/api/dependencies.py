from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from collections.abc import AsyncGenerator
from app.auth.jwt import verify_token
from app.models.users import User
from app.core.contextvars import request_context
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.repositories.user_repository import UserRepository
from app.database.unit_of_work import UnitOfWork
from app.services.company_auth import CompanyService
from app.services.invite_service import InviteService
from app.services.accept_invite import AcceptInviteService
from app.services.register import RegisterService
from app.services.authenticate import AuthenticationService
from app.services.role import has_permission
from app.domain.exceptions import (
    TenantMismatchError,
    InvalidTokenPayloadError,
    UserNotFoundError,
    PermissionDeniedError,
)
security = HTTPBearer()

# Unit of Work
async def get_uow(db:AsyncSession = Depends(get_db)) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(db) as uow:
        yield uow

# Authentication
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    uow:UnitOfWork = Depends(get_uow),
) -> User:

    # Verify token structured first (fast fail)
    payload = verify_token(credentials.credentials)
    user_id = payload.id

    if not user_id:
        raise InvalidTokenPayloadError("Invalid token payload")

    # DB Lookup
    user = await uow.users.get_by_id(payload.id)
    if user is None:
        raise UserNotFoundError("User not found")
    
    # Validate tenant claim
    if payload.tenant_id != str(user.tenant_id):
        raise TenantMismatchError("Tenant mismatch")

    # set context
    ctx = request_context.get()
    ctx.user_id = user.id
    ctx.tenant_id = user.tenant_id
    ctx.role = user.role

    return user

# Permission
def require_permission(permission: str, resource: str = "global"):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user.role, permission, resource):
            raise PermissionDeniedError(
                f"Permission denied: {resource}:{permission}",
            )
        return current_user

    return checker

# Services
def get_company_service(uow: UnitOfWork = Depends(get_uow)):
    return CompanyService(uow)

def get_invite_service(uow:UnitOfWork = Depends(get_uow)) -> InviteService:
    return InviteService(uow)

def get_accept_invite_service(uow:UnitOfWork = Depends(get_uow)) ->  AcceptInviteService:
    return AcceptInviteService(uow)

# def get_email_service() -> EmailService:
#     return get_email_service()

def get_reg_service(uow:UnitOfWork = Depends(get_uow)) -> RegisterService:
    return RegisterService(uow)

def get_auth_service(uow:UnitOfWork = Depends(get_uow)) -> AuthenticationService:
    return AuthenticationService(uow)