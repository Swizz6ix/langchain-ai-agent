from __future__ import annotations
from uuid import UUID
from typing import Generic, TypeVar
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")

class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> T | None:
        result = await self.session.execute(
            select(self.model)
                .where(
                    self.model.id == id
                )
            )
             
        return result.scalar_one_or_none()

    async def get_by_email_and_tenant(self, email, tenant_id) -> T | None:
        src = select(self.model).where(
            and_(
                self.model.email == email,
                self.model.tenant_id == tenant_id,
            )
        )
        result = await self.session.execute(src)
        return result.scalar_one_or_none()

    async def get_by_id_and_tenant(self, entity_id: UUID, tenant_id: UUID) -> T | None:
        src = select(self.model).where(
            self.model.id == entity_id,
            self.model.tenant_id == tenant_id,
        )

        result = await self.session.execute(src)
        return result.scalar_one_or_none()


    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def add_many(self, entities: list[T]) -> list[T]:
        self.session.add_all(entities)
        return entities
    
    async def create(self, entity: T) -> T:
        self.session.add(entity)

        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: T) -> T:
        await self.session.flush()
        await self.session.refresh(entity)

    async def delete(self, enity: T) -> None:
        await self.session.delete(enity)

    async def list(self) -> list[T]:
        result = await self.session.execute(
            select(self.model)
        )

        return result.scalars().all()