from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException
from db.models import Video
from db.services.base import BaseService


class VideoService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Video

    async def retrieve(self, id: str) -> Video:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.exec(statement)
        result = results.first()
        if not result:
            raise NotFoundException()
        return result
