import io
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from fastapi.responses import StreamingResponse

from core.containers import Container

from core.dependencies import get_current_user_id, get_db_session
from database.ext import managed_db_session
from schemas.todo_task.request import CreateToDoTask
from schemas.todo_task.response import ToDoTaskResponse
from services.todo_report import TodoReportService
from services.todo_task import ToDoTaskService
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

import uuid

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


@router.get(
    path="/", response_model=List[ToDoTaskResponse]
)  # todo: add params date from, date to, sorting, states
@inject
@managed_db_session()
async def get_tasks(
    offset: int = 0,
    limit: int = 100,  # todo: filters: move params to separate class
    todo_task_service: ToDoTaskService = Depends(
        dependency=Provide[Container.todo_task_service]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> List[ToDoTaskResponse]:
    return await todo_task_service.with_session(
        session=db_session
    ).get_user_all_todo_tasks(offset=offset, limit=limit, user_id=current_user_id)


@router.get(path="/{todo_task_id}", response_model=ToDoTaskResponse)
@inject
@managed_db_session()
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

    return todo_task


@router.get("/export/excel")
@inject
@managed_db_session()
async def export_todo_tasks(
    todo_task_service: ToDoTaskService = Depends(
        dependency=Provide[Container.todo_task_service]
    ),
    todo_report_service: TodoReportService = Depends(
        dependency=Provide[Container.todo_report_service]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(
        get_db_session
    ),  # todo: add params date from, date to, sorting, states
):
    """
    Экспорт todo задач пользователя в Excel файл
    """
    todo_tasks = await todo_task_service.with_session(
        session=db_session
    ).get_user_all_todo_tasks(offset=0, limit=None, user_id=current_user_id)

    # Создаем Excel файл
    excel_buffer = todo_report_service.create_excel_buffer(
        todos=todo_tasks,
    )

    # Формируем имя файла
    filename = f"todos_{uuid.uuid4()}.xlsx"  # todo: replace to user+time

    # Возвращаем файл
    return StreamingResponse(
        content=io.BytesIO(initial_bytes=excel_buffer.read()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
