from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class ToDoTask(Base):
    __tablename__ = "todo_tasks"
    name: Mapped[str] = mapped_column(String(255), unique=True)