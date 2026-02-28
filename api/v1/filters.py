from datetime import datetime
from fastapi import Depends, Query
from typing import Annotated
from pydantic import AfterValidator
from resources.constants import DATETIME_FMT, LIMIT_FROM_DEFAULT, LIMIT_TO_DEFAULT, OFFSET_FROM_DEFAULT
from resources.regex import HTTP_QUERY_DT_PATTERN


from schemas.query_params.query_params import (
    PaginationParams,
    SortingParams,
    SortOrder,
    DateRangeFilter,
)
from schemas.todo_task.query_params import ToDoTaskListParams




def parse_strict_datetime(datetime_str: str | None) -> datetime | None:
    if datetime_str is None:
        return None
    return datetime.strptime(datetime_str, DATETIME_FMT)


StrictDateTimeQuery = Annotated[
    str | None,
    Query(
        description=(
            "Формат: YYYY-MM-DDTHH:MM:SS\n"
            "Пример: 2026-02-14T12:30:00"
        ),
        pattern=HTTP_QUERY_DT_PATTERN,
    ),
    AfterValidator(parse_strict_datetime),
]


def get_todo_task_filter(
    date_from: StrictDateTimeQuery = None,
    date_to: StrictDateTimeQuery = None,
) -> DateRangeFilter:
    return DateRangeFilter(date_from=date_from, date_to=date_to)


def get_pagination_params(
    offset: int = Query(default=None, ge=OFFSET_FROM_DEFAULT, description="Смещение"),
    limit: int = Query(default=None, ge=LIMIT_FROM_DEFAULT, le=LIMIT_TO_DEFAULT, description="Лимит"),
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit)


def get_sorting_params(
    sort_by: str | None = Query(default=None, description="Поле сортировки"),
    sort_order: SortOrder | None = Query(default=None, description="Направление"),
) -> SortingParams:
    return SortingParams(sort_by=sort_by, sort_order=sort_order)


def get_dt_range_filter(
    date_from: Annotated[datetime, Query()],
    date_to: Annotated[datetime, Query()],
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
