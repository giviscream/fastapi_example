from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DeclarativeBase
from uuid import UUID
from datetime import datetime, timezone


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
