from sqlalchemy import Boolean, String
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todo_task import ToDoTask


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(500), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, server_default="0")
    password_hash: Mapped[str] = mapped_column(String(1000))

    tasks: Mapped[list["ToDoTask"]] = relationship(
        argument="ToDoTask",
        back_populates="responsible",
        cascade="all, delete-orphan",
    )
