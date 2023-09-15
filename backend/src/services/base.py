from typing import List, Union

from src.repositories.base import BaseRepository
from src.schemas import BaseModel


class BaseService:
    model: BaseModel = None

    def __init__(self):
        self.repo = BaseRepository()

    async def list(self, **kwargs) -> List[BaseModel]:
        return [self.model.model_validate(model) for model in await self.repo.list(**kwargs)]

    async def retrieve(self, id: Union[int, str]) -> BaseModel:
        return self.model.model_validate(await self.repo.retrieve(id))

    async def create(self, data: BaseModel) -> BaseModel:
        return self.model.model_validate(await self.repo.create(data.model_dump()))

    async def update(self, id: Union[int, str], data: BaseModel) -> BaseModel:
        return self.model.model_validate(await self.repo.update(id, data.model_dump()))

    async def delete(self, id: Union[int, str]) -> None:
        await self.repo.delete(id)
