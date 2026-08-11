import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import BaseModel
from app.models.types import UUIDPrimaryKey

class Tenant(BaseModel):
    __tablename__ = "tenants"

    id: Mapped[UUIDPrimaryKey] 

    name: Mapped[str] = mapped_column(
        String(100),
        unique = True,
        nullable = False,
    )

    users = relationship(
        "User",
        back_populates = "tenant",
        cascade = "all, delete-orphan",
    )