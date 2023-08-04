from sqlalchemy.ext.asyncio.session import AsyncSession

import src.models as pyd_models
from src.db import models as db_models
from src.db.services.base import BaseService


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.Message
        self.pydantic_model = pyd_models.Message
