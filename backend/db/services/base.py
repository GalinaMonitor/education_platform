from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException


class BaseService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = None
        self.pydantic_model = None

    async def list(self, **kwargs) -> List:
        statement = select(self.model)
        for key, value in kwargs.items():
            statement = statement.where(getattr(self.model, key) == value)
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return [self.pydantic_model.from_orm(model) for model in results]

    async def retrieve(self, id: int):
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return self.pydantic_model.from_orm(result)

    async def create(self, data):
        new_model = self.model(**data.dict())
        self.session.add(new_model)
        await self.session.commit()
        return self.pydantic_model.from_orm(new_model)

    async def update(self, id: int, data):
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        model = results.scalar_one_or_none()
        if not model:
            raise NotFoundException()
        for key, value in data.dict(exclude_unset=True).items():
            setattr(model, key, value)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self.pydantic_model.from_orm(model)

    async def delete(self, id: int) -> None:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        model = results.scalar_one_or_none()
        if not model:
            raise NotFoundException()
        await self.session.delete(model)
        await self.session.commit()
