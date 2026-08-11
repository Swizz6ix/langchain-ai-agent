from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.services.company_auth import CompanyService
from app.models.company_registration_request import CompanyRegistrationRequest
from app.models.users import User
from app.api.dependencies import get_company_service, require_permission

router = APIRouter(prefix="/company", tags=["Company Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_comp(request: CompanyRegistrationRequest, service: CompanyService = Depends(get_company_service)):
    return await service.register(request)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    service: CompanyService = Depends(get_company_service),
    current_user: User = Depends(require_permission("delete", "user")),
) -> None:
    await service.delete_user(current_user, user_id)

    return None

    

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    service: CompanyService = Depends(get_company_service),
    current_user: User = Depends(require_permission("delete", "tenant")),
) -> None:
    await service.delete_company(current_user)