from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from uuid import UUID, uuid4
from datetime import datetime, timezone


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
