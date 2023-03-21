from sqlmodel.ext.asyncio.session import AsyncSession

from db.models.all_models import Message
from db.services.base import BaseService


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Message
