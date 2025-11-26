from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from core.containers import Container

from core.dependencies import get_current_user_id, get_db_session
from database.ext import managed_db_session
from schemas.todo_task.request import CreateToDoTask
from schemas.todo_task.response import ToDoTaskResponse
from services.todo_task import ToDoTaskService
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    path="/",
    response_model=ToDoTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
@managed_db_session()
async def create_todo_task(
    todo_task_create: CreateToDoTask,
    todo_task_service: ToDoTaskService = Depends(Provide[Container.todo_task_service]),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> ToDoTaskResponse:
    try:
        return await todo_task_service.with_session(
            session=db_session
        ).create_todo_task(
            responsible_id=current_user_id,
            todo_task_create=todo_task_create,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(path="/", response_model=List[ToDoTaskResponse])
@inject
@managed_db_session()
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    todo_task_service: ToDoTaskService = Depends(
        dependency=Provide[Container.todo_task_service]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> List[ToDoTaskResponse]:
    return await todo_task_service.with_session(
        session=db_session
    ).get_user_all_todo_tasks(skip=skip, limit=limit, user_id=current_user_id)


@router.get(path="/{todo_task_id}", response_model=ToDoTaskResponse)
@inject
async def get_todo_task(
    todo_task_id: UUID,
    todo_task_service: ToDoTaskService = Depends(
        dependency=Provide[Container.todo_task_service]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> ToDoTaskResponse:
    todo_task: ToDoTaskResponse = await todo_task_service.with_session(
        session=db_session
    ).get_user_todo_task(task_id=todo_task_id, user_id=current_user_id)
    if not todo_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return todo_task
