from app.repositories.user_repository import UserRepository
from app.models.tenant import Tenant
from app.models.users import User
from app.auth.password import hash_password
from app.services.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company_registration_request import CompanyRegistrationRequest
from app.database.unit_of_work import UnitOfWork
from app.domain.exceptions import EmailAlreadyExistsError
from app.services.base_service import BaseService
from app.domain.exceptions import (
    PermissionDeniedError,
    UserNotFoundError,
    TenantNotFoundError,
    UnathorizedTenantAccessError
)

class CompanyService(BaseService):

    async def register(self, request: CompanyRegistrationRequest):
        existing = await self.uow.users.get_by_email(
            request.email,
        )
        
        if existing:
            raise EmailAlreadyExistsError()

        tenant = Tenant(name = request.company_name)

        await self.uow.tenants.create(tenant)

        admin = User(
            email = request.email,
            hash_password = hash_password(request.password),
            role = Role.ADMIN,
            tenant_id = tenant.id
        )

        await self.uow.users.create(admin)

        return admin

    async def delete_user(self, user_id, current_user):
        user = await self.uow.users.get_by_id_and_tenant(
            user_id,
            current_user.tenant_id,
        )

        if user is None:
            raise UserNotFoundError()

        if user.id == current_user.id:
            raise PermissionDeniedError()

        if user.id != current_user.user_id:
            raise UserNotFoundError()

        await self.uow.users.delete(user)

        return None

    async def delete_company(self, current_user):
        tenant = await self.uow.tenants.get_by_id(current_user.tenant_id)

        if tenant is None:
            raise TenantNotFoundError()

        await self.uow.tenants.delete(tenant)

        return None