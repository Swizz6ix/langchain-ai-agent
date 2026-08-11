from typing import Annotated
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from app.models.types import UUIDPrimaryKey, Timestamp

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[UUIDPrimaryKey]

    created_at: Mapped[Timestamp]

    updated_at: Mapped[Timestamp] = mapped_column(
        onupdate = datetime.now(timezone.utc)
    )