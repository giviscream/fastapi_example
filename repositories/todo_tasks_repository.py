from models.todo_task import ToDoTask
from repositories.base import BaseRepository


class ToDoTaskRepository(BaseRepository[ToDoTask]):
    def __init__(
        self,
    ):
        super().__init__(model=ToDoTask)
