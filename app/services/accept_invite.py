from datetime import datetime, timezone
from uuid import UUID
from app.services.base_service import BaseService
from app.models.users import User
from app.auth.password import hash_password
from app.services.role import Role
from app.models.accept_invite import AcceptInviteRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.invite_token import verify_invite_token
from app.domain.exceptions import (
    InvalidInviteError,
    InviteExpiredError,
    InviteAlreadyAcceptedError,
    EmailAlreadyExistsError,
    InviteRevokedError
)

class AcceptInviteService(BaseService):
    def __init__(self, uow):
        super().__init__(uow)

    async def accept_invite(self, request:AcceptInviteRequest) -> User:
        # Verify JWT signature and expiry (stateless, no DB hit)
        try:
            payload = verify_invite_token(request.token)

        except ValueError as exc:
            raise InvalidInviteError(str(exc))

        invite_id = UUID(payload["sub"])

        # load invite from DB to check bussiness state (accepted? revoked?)
        invite = await self.uow.invites.get_by_id(invite_id)

        if invite is None:
            raise InvalidInviteError("Invite not found")
        
        if invite.expires_at < datetime.now(timezone.utc):
            raise InviteExpiredError()

        if invite.revoked_at:
            raise InviteRevokedError("This invite has been revoked")

        if invite.email != payload["email"] or str(invite.tenant_id) != payload["tenant_id"]:
            raise InvalidInviteError("Token mismatch")

        existing_user = await self.uow.users.get_by_email (invite.email)

        # Idempotency: If already accepted, return the existing user
        if invite.accepted:
            if existing_user:
                return existing_user
            raise InviteAlreadyAcceptedError()

        # Idempotency: double click protection
        # if user somehow already exists (race condition) return them
        if existing_user:
            if existing_user.tenant_id == invite.tenant_id:
                invite.accepted = True
                invite.acceped_at = datetime.now(timezone.utc)
                return existing_user
            raise EmailAlreadyExistsError("Error already exist")

        invite.accepted = True
        invite.accepted_at = datetime.now(timezone.utc)

        user = User(
            email = invite.email,
            hash_password = hash_password(request.password),
            role = invite.role,
            tenant_id = invite.tenant_id,
        )

        await self.uow.users.create(user)
       
        return user