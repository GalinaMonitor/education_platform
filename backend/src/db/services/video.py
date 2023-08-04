from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

import src.models as pyd_models
from src.db import models as db_models
from src.db.services.base import BaseService
from src.exceptions import NotFoundException


class VideoService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.Video
        self.pydantic_model = pyd_models.Video

    async def retrieve(self, id: str) -> pyd_models.Video:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return self.pydantic_model.from_orm(result)
