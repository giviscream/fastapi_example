from uuid import UUID
from fastapi import APIRouter, Depends, status
from typing import Callable, List

from fastapi.responses import StreamingResponse

from api.v1.filters import get_dt_range_filter, get_todo_task_list_params
from core.containers import Container

from core.dependencies import get_current_user_id, get_db_session
from database.ext import managed_db_session
from resources.constants import (
    CONTENT_DISPOSITION_HEADER,
    CONTENT_DISPOSITION_TEMPLATE,
    FILENAME_TEMPLATE,
    REPORT_EXPORT_MEDIA_TYPE,
)
from schemas.query_params.query_params import DateRangeFilter
from schemas.todo_task.query_params import ToDoTaskListParams
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
    todo_task_service: Callable[..., ToDoTaskService] = Depends(
        dependency=Provide[Container.todo_task_service.provider]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> ToDoTaskResponse:
    return await todo_task_service(session=db_session).create_todo_task(
        responsible_id=current_user_id,
        todo_task_create=todo_task_create,
    )


@router.get(path="/", response_model=List[ToDoTaskResponse])
@inject
@managed_db_session()
async def get_todo_tasks(
    list_params: ToDoTaskListParams = Depends(get_todo_task_list_params),
    todo_task_service: Callable[..., ToDoTaskService] = Depends(
        dependency=Provide[Container.todo_task_service.provider]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> List[ToDoTaskResponse]:
    return await todo_task_service(session=db_session).get_user_all_todo_tasks(
        user_id=current_user_id,
        list_params=list_params,
    )


@router.get(path="/{todo_task_id}", response_model=ToDoTaskResponse)
@inject
@managed_db_session()
async def get_todo_task(
    todo_task_id: UUID,
    todo_task_service: Callable[..., ToDoTaskService] = Depends(
        dependency=Provide[Container.todo_task_service.provider]
    ),
    db_session: AsyncSession = Depends(get_db_session),
    current_user_id: UUID = Depends(get_current_user_id),
) -> ToDoTaskResponse:
    return await todo_task_service(session=db_session).get_user_todo_task(
        task_id=todo_task_id, user_id=current_user_id
    )


@router.get("/export/excel")
@inject
@managed_db_session()
async def export_todo_tasks(
    tasks_range: DateRangeFilter = Depends(get_dt_range_filter),
    todo_task_service: Callable[..., ToDoTaskService] = Depends(
        dependency=Provide[Container.todo_task_service.provider]
    ),
    todo_report_service: TodoReportService = Depends(
        dependency=Provide[Container.todo_report_service]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    """
    Экспорт todo задач пользователя в Excel файл
    """
    todo_tasks: List[ToDoTaskResponse] = await todo_task_service(
        session=db_session
    ).get_user_all_todo_tasks(
        user_id=current_user_id,
        list_params=ToDoTaskListParams(dt_range_filter=tasks_range),
    )

    filename = FILENAME_TEMPLATE.format(id=uuid.uuid4())

    return StreamingResponse(
        content=todo_report_service.get_report_chunks(todos=todo_tasks),
        media_type=REPORT_EXPORT_MEDIA_TYPE,
        headers={
            CONTENT_DISPOSITION_HEADER: CONTENT_DISPOSITION_TEMPLATE.format(
                filename=filename
            )
        },
    )
