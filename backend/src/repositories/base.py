from typing import List, Sequence, Union

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import get_session
from src.db.models import Base
from src.exceptions import NotFoundException


class BaseRepository:
    model: Base = None

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session

    async def list(self, **kwargs) -> Sequence[dict]:
        statement = select(self.model)
        for key, value in kwargs.items():
            statement = statement.where(getattr(self.model, key) == value)
        statement = statement.order_by(getattr(self.model, "id"))
        results = await self._session.execute(statement)
        return results.scalars().all()

    async def retrieve(self, id: Union[int, str]) -> dict:
        statement = select(self.model).where(self.model.id == id)
        results = await self._session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return result

    async def create(self, data: dict) -> dict:
        new_model = self.model(**data)
        self._session.add(new_model)
        await self._session.flush()
        return new_model

    async def update(self, id: Union[int, str], data: dict) -> dict:
        statement = select(self.model).where(self.model.id == id)
        results = await self._session.execute(statement)
        model = results.scalar_one_or_none()
        if not model:
            raise NotFoundException()
        for key, value in data.items():
            setattr(model, key, value)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model

    async def update_all(self, ids: List[Union[int, str]], data: dict) -> dict:
        statement = update(self.model).where(self.model.id.in_(ids)).values(data).returning(self.model)
        results = await self._session.scalars(statement)
        await self._session.flush()
        return results.all()

    async def delete(self, id: int) -> None:
        statement = select(self.model).where(self.model.id == id)
        results = await self._session.execute(statement)
        model = results.scalar_one_or_none()
        if not model:
            raise NotFoundException()
        await self._session.delete(model)
        await self._session.flush()
