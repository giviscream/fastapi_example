from datetime import datetime
from typing import Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, delete, update, insert
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: type[ModelType],
    ):
        self.model = model

    def _apply_pagination(
        self,
        query: Select,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Select:
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query

    def _apply_sorting(
        self,
        query: Select,
        sort_by: str | None = None,
        sort_order: str = "asc",
    ) -> Select:
        if sort_by is None:
            return query

        column = getattr(self.model, sort_by, None)
        if column is None:
            return query

        order_func = asc if sort_order == "asc" else desc
        return query.order_by(order_func(column))

    def _apply_range_filters(
        self,
        query: Select,
        *,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> Select:

        if date_from is not None:
            query = query.where(self.model.created_at >= date_from)
        if date_to is not None:
            query = query.where(self.model.created_at <= date_to)
        return query

    async def get_by_id(self, session: AsyncSession, id: UUID) -> Optional[ModelType]:
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one()

    async def get_one(self, session: AsyncSession, **filters) -> Optional[ModelType]:
        result = await session.execute(select(self.model).filter_by(**filters))
        return result.scalar_one()

    async def list(
        self,
        session: AsyncSession,
        offset: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        **filters,
    ) -> list[ModelType]:

        stmt = select(self.model).filter_by(**filters)
        stmt = self._apply_sorting(stmt, sort_by=sort_by, sort_order=sort_order)
        stmt = self._apply_pagination(stmt, offset=offset, limit=limit)
        stmt = self._apply_range_filters(stmt, date_from=date_from, date_to=date_to)

        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, **instance_data) -> ModelType:
        result = await session.execute(
            insert(self.model).values(**instance_data).returning(self.model)
        )
        return result.scalar_one()

    async def update(
        self, session: AsyncSession, id: int, **instance_data
    ) -> ModelType:
        await session.execute(
            update(self.model).where(self.model.id == id).values(**instance_data)
        )

    async def delete(self, session: AsyncSession, id: int) -> None:
        await session.execute(delete(self.model).where(self.model.id == id))
