from typing import List

from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException


class BaseService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = None

    async def list(self, **kwargs) -> List[SQLModel]:
        statement = select(self.model)
        for key, value in kwargs.items():
            statement = statement.where(getattr(self.model, key) == value)
        results = await self.session.exec(statement)
        result = results.all()
        return result

    async def retrieve(self, id: int) -> SQLModel:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.exec(statement)
        result = results.first()
        if not result:
            raise NotFoundException()
        return result

    async def create(self, data: SQLModel) -> SQLModel:
        new_model = self.model(**data.dict())
        self.session.add(new_model)
        await self.session.commit()
        return new_model

    async def update(self, id: int, data: SQLModel) -> SQLModel:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.exec(statement)
        model = results.first()
        if not model:
            raise NotFoundException()
        for key, value in data.dict(exclude_unset=True).items():
            setattr(model, key, value)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def delete(self, id: int) -> None:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.exec(statement)
        model = results.first()
        if not model:
            raise NotFoundException()
        await self.session.delete(model)
        await self.session.commit()
