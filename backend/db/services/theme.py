from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.db.models import Theme as ThemeDB
from backend.db.services.base import BaseService
from backend.models import Theme


class ThemeService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = ThemeDB
        self.pydantic_model = Theme
