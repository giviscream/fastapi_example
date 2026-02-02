from typing import Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, insert
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: type[ModelType],
    ):
        self.model = model

    async def get_by_id(self, session: AsyncSession, id: UUID) -> Optional[ModelType]:
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one()

    async def get_one(self, session: AsyncSession, **kwargs) -> Optional[ModelType]:
        result = await session.execute(select(self.model).filter_by(**kwargs))
        return result.scalar_one()

    async def list(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **filters,
    ) -> list[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)

        if filters:
            stmt = stmt.filter_by(**filters)

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
