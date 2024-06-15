from typing import Union

from fastapi import Depends
from pydantic import parse_obj_as

from src.repositories.message import MessageRepository
from src.schemas import BaseModel, Message
from src.services.base import BaseService


class MessageService(BaseService):
    model = Message

    def __init__(self, repo: MessageRepository = Depends()):
        super().__init__()
        self.repo = repo

    async def update_all(self, ids: list[int], data: BaseModel) -> list[Message]:
        return parse_obj_as(list[self.model], await self.repo.update_all(ids, data.model_dump()))
