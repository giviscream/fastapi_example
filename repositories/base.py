from typing import Generic, Optional, TypeVar

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase

# T = TypeVar('T')
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.all()

    async def create(self, **instance_data) -> ModelType:
        instance = self.model(**instance_data)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, id: int, **instance_data) -> ModelType:
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(**instance_data)
        )

    async def delete(self, id: int) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == id))
