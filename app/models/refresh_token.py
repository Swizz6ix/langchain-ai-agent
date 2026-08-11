from uuid import UUID
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import BaseModel
from app.models.types import UUIDPrimaryKey, Timestamp

class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUIDPrimaryKey]

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index = True,
        nullable = False,
    )

    token_hash: Mapped[str]

    expires_at: Mapped[Timestamp]

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
        nullable = False,
    )