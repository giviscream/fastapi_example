from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    offset: int = Field(default=0, ge=0, description="Смещение")
    limit: int = Field(default=100, ge=1, le=1000, description="Лимит")


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortingParams(BaseModel):
    sort_by: Optional[str] = Field(default=None, description="Поле сортировки")
    sort_order: SortOrder = Field(default=SortOrder.ASC, description="Направление")


class DateRangeFilter(BaseModel):
    date_from: datetime | None = Field(default=None, description="Дата от")
    date_to: datetime | None = Field(default=None, description="Дата до")
