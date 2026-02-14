from datetime import datetime
from fastapi import Depends, Query

from schemas.query_params.query_params import (
    PaginationParams,
    SortingParams,
    SortOrder,
    DateRangeFilter,
)
from schemas.todo_task.query_params import ToDoTaskListParams


def get_pagination_params(
    offset: int = Query(default=0, ge=0, description="Смещение"),
    limit: int = Query(default=100, ge=1, le=1000, description="Лимит"),
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit)


def get_sorting_params(
    sort_by: str | None = Query(default=None, description="Поле сортировки"),
    sort_order: SortOrder = Query(default=SortOrder.ASC, description="Направление"),
) -> SortingParams:
    return SortingParams(sort_by=sort_by, sort_order=sort_order)


def get_dt_range_filter(
    date_from: datetime | None = Query(
        default=None,
        description="Дата и время от (ISO 8601). Пример: 2026-02-14T12:30:00Z",
        examples=["2026-02-14T12:30:00Z"],
    ),
    date_to: datetime | None = Query(
        default=None,
        description="Дата и время до (ISO 8601). Пример: 2026-02-14T18:00:00+03:00",
        examples=["2026-02-14T18:00:00+03:00"],
    ),
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
