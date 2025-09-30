from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class ToDoTask(Base):
    name: Mapped[str] = mapped_column(String(255), unique=True)