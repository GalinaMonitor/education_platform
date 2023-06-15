from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.models import Video as VideoDB
from db.services.base import BaseService
from exceptions import NotFoundException
from models import Video


class VideoService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = VideoDB
        self.pydantic_model = Video

    async def retrieve(self, id: str) -> Video:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return self.pydantic_model.from_orm(result)
