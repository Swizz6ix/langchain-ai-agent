from typing import Dict, Type

from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DomainError,
    EmailAlreadyExistsError,
    InviteExpiredError,
    InviteAlreadyAcceptedError,
    InviteRevokedError,
    InvalidInviteError,
    InviteNotFoundError,
    InvalidCredentialsError,
    UserNotFoundError,
    UnathorizedTenantAccessError,
    PermissionDeniedError,
    PendingInviteExistsError,
    TenantNotFoundError,
    TenantMismatchError,
    InvalidTokenPayloadError,
)

EXCEPTION_STATUS_CODES: Dict[Type[DomainError], int] = {
    EmailAlreadyExistsError: status.HTTP_409_CONFLICT,
    InviteAlreadyAcceptedError: status.HTTP_409_CONFLICT,
    PendingInviteExistsError: status.HTTP_409_CONFLICT,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    TenantNotFoundError: status.HTTP_404_NOT_FOUND,
    InviteNotFoundError: status.HTTP_404_NOT_FOUND,
    UnathorizedTenantAccessError: status.HTTP_403_FORBIDDEN,
    TenantMismatchError: status.HTTP_403_FORBIDDEN,
    PermissionDeniedError: status.HTTP_401_UNAUTHORIZED,
    InvalidTokenPayloadError: status.HTTP_401_UNAUTHORIZED,
    InviteExpiredError: status.HTTP_400_BAD_REQUEST,
    InvalidInviteError: status.HTTP_400_BAD_REQUEST,
    InvalidCredentialsError: status.HTTP_400_BAD_REQUEST,
    InviteRevokedError: status.HTTP_400_BAD_REQUEST,
}

async def domain_exception_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code = EXCEPTION_STATUS_CODES.get(
        type(exc),
        status.HTTP_400_BAD_REQUEST,
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "detail": str(exc) or exc.__class__.__name__,
        },
    )

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        DomainError,
        domain_exception_handler,
    )