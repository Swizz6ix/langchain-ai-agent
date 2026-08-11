from datetime import datetime
import uuid
from sqlalchemy import String, ForeignKey, Uuid, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.services.role import Role
from app.models.mixins import BaseModel
from app.models.types import NullableTimestamp, Email, UUIDPrimaryKey

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUIDPrimaryKey]

    email: Mapped[Email]

    hash_password: Mapped[str]

    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, native_enum=False),
        nullable = False
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        index = True,
        nullable = False,
    )

    tenant = relationship(
        "Tenant",
        back_populates = "users"
    )

    deleted_at: Mapped[NullableTimestamp]