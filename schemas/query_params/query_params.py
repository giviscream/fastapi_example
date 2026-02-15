from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    offset: int | None = Field(default=None, ge=0, description="Смещение")
    limit: int | None = Field(default=None, ge=1, le=1000, description="Лимит")


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortingParams(BaseModel):
    sort_by: str | None = Field(default=None, description="Поле сортировки")
    sort_order: SortOrder | None = Field(default=None, description="Направление")


class DateRangeFilter(BaseModel):
    date_from: datetime | None = Field(default=None, description="Дата от")
    date_to: datetime | None = Field(default=None, description="Дата до")
