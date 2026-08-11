from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from app.models.invitation import Invitation
from app.models.invite_request import InviteRequest
from app.services.role import _normalize_role
from app.services.base_service import BaseService
from app.repositories.user_repository import UserRepository
from app.repositories.invitation_repository import InvitationRepository
from app.database.unit_of_work import UnitOfWork
from app.services.role import Role, has_permission
from app.auth.invite_token import create_invite_token
from app.domain.exceptions import (
    EmailAlreadyExistsError, 
    PendingInviteExistsError,
    PermissionDeniedError,
    InviteNotFoundError,
    InviteAlreadyAcceptedError,
    InviteRevokedError,
)

class InviteService(BaseService):
    def __init__(self, uow):
        super().__init__(uow)

    async def send_invite(
        self,
        request: InviteRequest,
        current_user_id: UUID, 
        current_tenant_id: UUID,
        current_user_role: str
    ) -> tuple[Invitation, str]:

        if current_user_role != Role.ADMIN:
            raise PermissionDeniedError()
        
        # Idempoteny: If client sent a key, return existing invite
        if request.idempotency_key:
            existing = await self.uow.invites.get_by_idempotency_key(request.idempotency_key)

            if existing:
                # re-return the same token so the email link is identical
                return existing, existing.token

        # Check if email already belongs to a user in this tenant
        existing_user = await self.uow.users.get_by_email_and_tenant(
            email = request.email,
            tenant_id = current_tenant_id
        )
        if existing_user:
            raise EmailAlreadyExistsError("User already belongs to this tenant")

        #check for pending invite
        pending = await self.uow.invites.get_pending_invitation(request.email, current_tenant_id)

        if pending:
            raise PendingInviteExistsError(
                "An active invite already exists for this email"
            )

        invite_id = uuid4()
        role = _normalize_role(request.role)

        token = create_invite_token(
            invite_id = str(invite_id),
            email =request.email,
            tenant_id = str(current_tenant_id),
            role = str(role),
        )

        invite = Invitation(
            id = invite_id,
            email = request.email,
            tenant_id = current_tenant_id,
            role = role or Role.USER,
            token = token,
            idempotency_key = request.idempotency_key,
            invited_by = current_user_id,
            expires_at = datetime.now(timezone.utc) + timedelta(days = 7),
        )

        await self.uow.invites.create(invite)

        return invite, token
    
    async def resend_invite(
            self,
            invite_id: UUID,
            current_user_id: UUID,
            current_user_role: str,
    ) -> tuple[Invitation, str]:

        if current_user_role != Role.ADMIN:
            raise PermissionDeniedError()
        
        invite = await self.uow.invites.get_by_id(invite_id)

        if invite is None:
            raise InviteNotFoundError("Invite not found")

        if invite.invited_by != current_user_id:
            raise PermissionDeniedError()

        can_resend_any = has_permission(current_user_role, "resend_any", "invite")

        if not can_resend_any:
            raise PermissionDeniedError()

        if invite.accepted:
            raise InviteAlreadyAcceptedError("Invite already accepted")

        if invite.revoked_at:
            raise InviteRevokedError("Invite has been revoked")

        last_sent = invite.updated_at or invite.created_at
        if datetime.now(timezone.utc) - last_sent < timedelta(hours=1):
            raise ValueError("please wait for an hour, before resending")

        # Regenerate JWT and bump expiry
        invite.token = create_invite_token(
            invite_id = str(invite_id),
            email = invite.email,
            tenant_id = str(invite.tenant_id),
            role = str(invite.role),
        )
        invite.expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        return invite, invite.token

    async def revoke_invite(
        self,
        invite_id: UUID,
        current_user_id: UUID,
        current_user_role: str,
    ) -> None:
        if current_user_role != Role.ADMIN:
            raise PermissionDeniedError()
       
        invite = await self.uow.invites.get_by_id(invite_id)
        if invite is None:
            raise InviteNotFoundError("invite not found")

        if invite.invited_by != current_user_id:
            raise PermissionDeniedError()

        can_resend_any = has_permission(current_user_role, "resend_any", "invite")
        
        if not can_resend_any:
            raise PermissionDeniedError()
        
        if invite.accepted:
            raise InviteAlreadyAcceptedError("Cannot rovoke an already accepted invite")

        if invite.revoked_at:
            raise

        invite.revoked_at = datetime.now(timezone.utc)
        invite.revoked_by_id = current_user_id

    async def list_invites(
        self,
        tenant_id: UUID,
        status: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Invitation], int]:
        offset = (page - 1) * limit

        invites = await self.uow.invites.list_by_tenant(
            tenant_id=tenant_id,
            status=status,
            offset=offset,
            limit=limit,
        )

        total = await self.uow.invites.count_by_tenant(
            tenant_id=tenant_id,
            status=status,
        )

        return invites, total

    async def bulk_send_invites(
        self,
        requests: list[InviteRequest],
        current_user_id: UUID,
        current_tenant_id: UUID,
    ) -> list[tuple[Invitation, str]]:
        """
        Atomic: Validates all emails first, then creates all invites.
        If any email fails validation, the entire batch is rejected.
        """

        if not requests:
            raise ValueError("No invites provided")

        emails = [req.email for req in requests]
        if len(emails) != len(set(emails)):
            raise ValueError("Duplicate emails in bulk request")

        created = []
        for req in requests:
            existing_user = await self.uow.users.get_by_email_and_tenant(
                req.email,
                current_tenant_id,
            )
            if existing_user:
                raise EmailAlreadyExistsError(f"User already exists: {req.email}")

            pending = await self.uow.invites.get_pending_invitation(
                req.email,
                current_tenant_id,
            )

            if pending:
                raise PendingInviteExistsError(f"Pending invite exists: {req.email}")

            invite_id = uuid4()
            role = _normalize_role(req.role)
            
            token = create_invite_token(
                invite_id = str(invite_id),
                email = req.email,
                tenant_id = str(current_tenant_id),
                role = str(role),
            )

            invite = Invitation(
                id = invite_id,
                email = req.email,
                tenant_id = current_tenant_id,
                role = role or Role.USER,
                token = token,
                invited_by = current_user_id,
                idempotency_key = req.idempotency_key,
                expires_at = datetime.now(timezone.utc) + timedelta(days=7),
            )
            created.append(invite)
        self.uow.invites.add_many(created)
        await self.uow.flush()

        return [(invite, invite.token) for invite in created]