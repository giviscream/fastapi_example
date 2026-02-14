from pydantic import BaseModel, Field

from schemas.query_params.query_params import PaginationParams, SortingParams, DateRangeFilter


class ToDoTaskListParams(BaseModel):
    pagination: PaginationParams = Field(default_factory=PaginationParams)
    sorting: SortingParams = Field(default_factory=SortingParams)
    dt_range_filter: DateRangeFilter = Field(default_factory=DateRangeFilter)
