from sqlalchemy.ext.asyncio.session import AsyncSession

import src.models as pyd_models
from src.db import models as db_models
from src.db.services.base import BaseService


class ThemeService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.Theme
        self.pydantic_model = pyd_models.Theme
