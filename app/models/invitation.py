from datetime import datetime
from uuid import UUID
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Uuid, ForeignKey
from sqlalchemy import Enum as SQLEnum
from app.services.role import Role
from app.models.mixins import BaseModel
from app.models.types import UUIDPrimaryKey, Email, Timestamp


class Invitation(BaseModel):
    __tablename__ = "invitations"

    id: Mapped[UUIDPrimaryKey]

    email: Mapped[Email]

    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index = True,
        nullable = True,
    )

    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, native_enum=False),
        nullable = False
    )

    token: Mapped[str] = mapped_column(
        String,
        unique = True,
        nullable = False,
        index = True,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String,
        unique = True,
        nullable = True,
        index = True,
    )

    accepted: Mapped[bool] = mapped_column(
        Boolean,
        default = False
    )

    expires_at: Mapped[Timestamp] = mapped_column(
        nullable = False,
    ) 

    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable = True
    )

    invited_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id")
    )

    tenant = relationship("Tenant")
    creator = relationship("User", foreign_keys=[invited_by])

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable = True
    )

    revoked_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable = True,
    )