from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.tenant_repository import TenantRepository
from app.repositories.invitation_repository import InvitationRepository
from app.repositories.refresh_repository import RefreshRepository
class UnitOfWork:
    def __init__(self, db:AsyncSession):
        self._db = db
        self._users = None
        self._tenants = None
        self._invites = None
        self._refresh = None

    @property
    def users(self) -> UserRepository:
        if self._users is None:
            self._users = UserRepository(self._db)
        return self._users

    @property
    def tenants(self) -> TenantRepository:
        if self._tenants is None:
            self._tenants = TenantRepository(self._db)
        return self._tenants

    @property
    def invites(self) -> InvitationRepository:
        if self._invites is None:
            self._invites = InvitationRepository(self._db)
        return self._invites
    
    @property
    def refresh(self) -> RefreshRepository:
        if self._refresh is None:
            self._refresh = RefreshRepository(self._db)
        return self._refresh

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.rollback()
            return False

        else:
            await self.save()
            return False

    async def save(self):
        await self._db.commit()

    async def rollback(self):
        await self._db.rollback()

    async def flush(self):
        await self._db.flush()
