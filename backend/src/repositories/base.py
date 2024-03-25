from typing import List, Sequence, Union

from sqlalchemy import select, update

from src.db.config import async_session
from src.db.models import Base
from src.exceptions import NotFoundException


class BaseRepository:
    model: Base = None

    async def list(self, **kwargs) -> Sequence[dict]:
        async with async_session() as session:
            statement = select(self.model)
            for key, value in kwargs.items():
                statement = statement.where(getattr(self.model, key) == value)
            statement = statement.order_by(getattr(self.model, "id"))
            results = await session.execute(statement)
            return results.scalars().all()

    async def retrieve(self, id: Union[int, str]) -> dict:
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            results = await session.execute(statement)
            result = results.scalar_one_or_none()
            if not result:
                raise NotFoundException()
            return result

    async def create(self, data: dict) -> dict:
        async with async_session() as session:
            new_model = self.model(**data)
            session.add(new_model)
            await session.commit()
            return new_model

    async def update(self, id: Union[int, str], data: dict) -> dict:
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            results = await session.execute(statement)
            model = results.scalar_one_or_none()
            if not model:
                raise NotFoundException()
            for key, value in data.items():
                setattr(model, key, value)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    async def update_all(self, ids: List[Union[int, str]], data: dict) -> dict:
        async with async_session() as session:
            statement = update(self.model).where(self.model.id.in_(ids)).values(data).returning(self.model)
            results = await session.scalars(statement)
            return results.all()

    async def delete(self, id: int) -> None:
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            results = await session.execute(statement)
            model = results.scalar_one_or_none()
            if not model:
                raise NotFoundException()
            await session.delete(model)
            await session.commit()
