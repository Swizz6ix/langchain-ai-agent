from datetime import datetime, timezone
import uuid
from sqlalchemy import Uuid, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

UUIDPrimaryKey = Annotated[
    uuid.UUID,
    mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    ),
]

Timestamp = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        default = datetime.now(timezone.utc)
    ),
]

NullableTimestamp = Annotated[
    datetime | None,
    mapped_column(DateTime(timezone=True), nullable=True)
]

Email = Annotated[
    str,
    mapped_column(
        String(255),
        index = True,
        nullable = False,
        unique = True
    )
]