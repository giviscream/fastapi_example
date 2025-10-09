from uuid import UUID
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User


class ToDoTask(Base):
    __tablename__ = "todo_tasks"
    title: Mapped[str] = mapped_column(String(500), comment="Заголовок задачи")
    description: Mapped[str] = mapped_column(String(5000), comment="Описание задачи")

    responsible_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="users.id", ondelete="SET NULL")
    )
    responsible: Mapped["User"] = relationship(
        argument="User",
        foreign_keys=[responsible_id],
        back_populates="tasks",
        lazy="select"
    )
