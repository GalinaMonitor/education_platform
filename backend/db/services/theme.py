from sqlmodel.ext.asyncio.session import AsyncSession

from db.models import Theme
from db.services.base import BaseService


class ThemeService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Theme
