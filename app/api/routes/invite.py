from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.invite_service import InviteService
from app.services.accept_invite import AcceptInviteService
from app.models.invite_request import InviteRequest, BulkInviteRequest
from app.models.accept_invite import AcceptInviteRequest
from app.models.users import User
from app.api.dependencies import (
    get_current_user, 
    get_accept_invite_service, 
    get_invite_service,
    require_permission,
)

router = APIRouter(prefix="/invite", tags = ["Invitation"])

@router.get("", status_code=status.HTTP_200_OK)
async def list_invites(
    status: Literal["all", "pending", "accepted", "revoked"] = Query("all"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: InviteService = Depends(get_invite_service),
    current_user: User = Depends(require_permission("list", "invite")),
):
    invites, total = await service.list_invites(
        tenant_id=current_user.tenant_id,
        status=None if status == "all" else status,
        page=page,
        limit=limit,
    )

    return {
        "data": [
            {
                "id": invite.id,
                "email": invite.email,
                "role": invite.role,
                "invited_by": invite.invited_by,
                "accepted": invite.accepted,
                "revoked_at": invite.revoked_at,
                "expires_at": invite.expires_at,
                "created_at": invite.created_at,
            }
            for invite in invites
        ],
        "total": total,
        "page": page,
        "limit": limit,
    }

@router.post("/invite_user", status_code=status.HTTP_201_CREATED)
async def invite_user(
    request:InviteRequest, 
    # background_tasks: BackgroundTasks,
    service: InviteService = Depends(get_invite_service),
    current_user: User = Depends(get_current_user),
):
    invite, token = await service.send_invite(
        request = request,
        current_user_id = current_user.id,
        current_tenant_id = current_user.tenant_id,
        current_user_role = current_user.role
    )

    return {
        "id": invite.id,
        "email": invite.email,
        "role": invite.role,
        "token": token,
        "invite_token": invite.token,
        "expires_at": invite.expires_at,
    }


    # background_tasks.add_task(
    #     invite_token = token,
    #     email = invite.email,
    #     invited_by_email = current_user.email,
    # )

    # return {
    #     "id": invite.id,
    #     "email": invite.email,
    #     "role": invite.role,
    #     "expires_at": invite.expires_at
    # }

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_invite(
    request: BulkInviteRequest,
    # background_tasks: BackgroundTasks,
    service: InviteService = Depends(get_invite_service),
    current_user: User = Depends(require_permission("bulk_send", "invite")),
):
    results = await service.bulk_send_invites(
        requests=request.invites,
        current_user_id=current_user.id,
        current_tenant_id=current_user.tenant_id,
    )

    # for invite, token in results:
        # background_tasks.add_task(
        #     email_service.send_invite_email,
        #     to_email = invite.email,
        #     invite_token = token,
        #     tenant_name = tenant.name,
        #     invited_by = current_user.email,
        # )
    return {
        "total_created": len(results),
        "invites": [
            {
                "id": invite.id,
                "email": invite.email,
                "role": invite.role,
                "token": token,
                "expires_at": invite.expires_at,
            }
            for invite, token in results
        ],
    }


@router.post("/{invite_id}/resend", status_code=status.HTTP_200_OK)
async def resend_invite(
    invite_id: UUID,
    service: InviteService = Depends(get_invite_service),
    current_user: User = Depends(get_current_user),
):
    invite, token = await service.resend_invite(
        invite_id = invite_id,
        current_user_id = current_user.id,
        current_user_role = current_user.role,
    )

    return {
        "id": invite.id,
        "email": invite.email,
        "role": invite.role,
        "token": token,
        "invite_token": invite.token,
        "expires_at": invite.expires_at,
    }

@router.delete("/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_inv(
    invite_id: UUID,
    service: InviteService = Depends(get_invite_service),
    current_user: User = Depends(get_current_user),
):
    await service.revoke_invite(
        invite_id = invite_id,
        current_user_id = current_user.id,
        current_user_role = current_user.role,
    )
    
    return None

@router.post("/accept", status_code=status.HTTP_201_CREATED)
async def accept_user(
    request:AcceptInviteRequest, 
    service: AcceptInviteService = Depends(get_accept_invite_service)
):
    user = await service.accept_invite(request)
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "tenant_id": user.tenant_id
    }

