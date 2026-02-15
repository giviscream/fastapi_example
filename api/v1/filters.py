from datetime import datetime
from fastapi import Depends, Query
from typing import Annotated
from pydantic import AfterValidator


from schemas.query_params.query_params import (
    PaginationParams,
    SortingParams,
    SortOrder,
    DateRangeFilter,
)
from schemas.todo_task.query_params import ToDoTaskListParams

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S"


def parse_strict_datetime(v: str | None) -> datetime | None:
    if v is None:
        return None
    try:
        return datetime.strptime(v, DATETIME_FMT)
    except ValueError:
        raise ValueError("Invalid datetime format. Expected YYYY-MM-DDTHH:MM:SS")


StrictDateTimeQuery = Annotated[
    str | None,
    Query(
        description="Формат: YYYY-MM-DDTHH:MM:SS",
        examples=["2026-02-14T12:30:00"],
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$",
    ),
    AfterValidator(parse_strict_datetime),
]


def get_todo_task_filter(
    date_from: StrictDateTimeQuery = None,
    date_to: StrictDateTimeQuery = None,
) -> DateRangeFilter:
    return DateRangeFilter(date_from=date_from, date_to=date_to)


def get_pagination_params(
    offset: int = Query(default=None, ge=0, description="Смещение"),
    limit: int = Query(default=None, ge=1, le=1000, description="Лимит"),
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit)


def get_sorting_params(
    sort_by: str | None = Query(default=None, description="Поле сортировки"),
    sort_order: SortOrder | None = Query(default=None, description="Направление"),
) -> SortingParams:
    return SortingParams(sort_by=sort_by, sort_order=sort_order)


def get_dt_range_filter(
    date_from: StrictDateTimeQuery = None,
    date_to: StrictDateTimeQuery = None,
) -> DateRangeFilter:
    return DateRangeFilter(date_from=date_from, date_to=date_to)


def get_todo_task_list_params(
    pagination: PaginationParams = Depends(get_pagination_params),
    sorting: SortingParams = Depends(get_sorting_params),
    dt_range_filter: DateRangeFilter = Depends(get_dt_range_filter),
) -> ToDoTaskListParams:
    return ToDoTaskListParams(
        pagination=pagination,
        sorting=sorting,
        dt_range_filter=dt_range_filter,
    )
