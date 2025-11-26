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
        session: AsyncSession | None = None,
    ):
        self.session = session
        self.model = model

    def with_session(self, session: AsyncSession):
        self.session = session
        return self

    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, **instance_data) -> ModelType:
        result = await self.session.execute(
            insert(self.model).values(**instance_data).returning(self.model)
        )
        return result.scalar_one()

    async def update(self, id: int, **instance_data) -> ModelType:
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(**instance_data)
        )

    async def delete(self, id: int) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == id))
