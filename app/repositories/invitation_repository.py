from uuid import UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, and_, func, delete
from app.models.invitation import Invitation
from app.repositories.base_repository import BaseRepository

class InvitationRepository(BaseRepository[Invitation]):
    model = Invitation

    async def get_pending_invitation(self, email: str, tenant_id):
        list = await self.session.execute(
            select(Invitation)
            .where(
                and_(
                    Invitation.email == email,
                    Invitation.tenant_id == tenant_id,
                    Invitation.accepted.is_(False),
                    Invitation.revoked_at.is_(None)
                )
            )
        )

        for result in list:
            return result.scalar_one_or_none()

        # return list(result.scalars())

    async def get_by_token(self, token: str) -> Invitation | None:
        result = await self.session.execute(
            select(Invitation).where(Invitation.token == token)
        )

        return result.scalar_one_or_none()

    async def get_by_idempotency_key(self, key: str) -> Invitation| None:
        result = await self.session.execute(
            select(Invitation)
            .where(
                Invitation.idempotency_key == key
            )
        )
        return result.scalar_one_or_none()
    
    async def list_by_tenant(
        self,
        tenant_id: UUID,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Invitation]:
        query = select(Invitation).where(Invitation.tenant_id == tenant_id)
        if status == "pending":
            query = query.where(
                Invitation.accepted.is_(False),
                Invitation.revoked_at.is_(None),
            )

        elif status == "accepted":
            query = query.where(Invitation.accepted.is_(True))

        elif status == "revoked":
            query = query.where(Invitation.revoked_at.isnot(None))

        query = query.order_by(Invitation.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(query)

        return list(result.scalars())

    async def count_by_tenant(
        self,
        tenant_id: UUID,
        status: str | None = None,
    ) -> int:
        query = select(func.count()).where(Invitation.tenant_id == tenant_id)

        if status == "pending":
            query = query.where(
                Invitation.accepted.is_(False),
                Invitation.revoked_at.is_(None),
            )

        elif status == "accepted":
            query = query.where(Invitation.accepted_at.is_(True))

        elif status == "revoked":
            query = query.where(Invitation.revoked_at.isnot(None))

        result = await self.session.execute(query)
        return result.scalar()

    async def delete_expired_invites(self):
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        src = (
            delete(Invitation)
            .where(Invitation.expires_at < cutoff)
            .where(Invitation.accepted_at.is_(False))
        )

        result = await self.session.execute(src)
        return result.rowcount
