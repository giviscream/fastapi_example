from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from core.containers import Container

# from core.dependencies import get_current_user
from core.dependencies import get_current_user_id
from schemas.todo_task.request import CreateToDoTask
from schemas.todo_task.response import ToDoTaskResponse
from schemas.user.response import UserResponse
from services.todo_task import ToDoTaskService
from dependency_injector.wiring import Provide, inject

router = APIRouter()


@router.post(
    path="/",
    response_model=ToDoTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_todo_task(
    todo_task_create: CreateToDoTask,
    todo_task_service: ToDoTaskService = Depends(Provide[Container.todo_task_service]),
    user_id: UserResponse = Depends(get_current_user_id),
) -> ToDoTaskResponse:
    try:
        return await todo_task_service.create_todo_task(
            responsible_id=user_id,
            todo_task_create=todo_task_create,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(path="/", response_model=List[ToDoTaskResponse])
@inject
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    todo_task_service: ToDoTaskService = Depends(
        dependency=Provide[Container.todo_task_service]
    ),
) -> List[ToDoTaskResponse]:
    return await todo_task_service.get_all_todo_tasks(skip=skip, limit=limit)


@router.get(path="/{todo_task_id}", response_model=ToDoTaskResponse)
@inject
async def get_todo_task(
    todo_task_id: int,
    todo_task_service: ToDoTaskService = Depends(
        dependency=Provide[Container.todo_task_service]
    ),
) -> ToDoTaskResponse:
    todo_task: ToDoTaskResponse = await todo_task_service.get_todo_task(todo_task_id)
    if not todo_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return todo_task
