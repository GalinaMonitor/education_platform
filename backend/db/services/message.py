from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.db.models import Message as MessageDB
from backend.db.services.base import BaseService
from backend.models import Message


class MessageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = MessageDB
        self.pydantic_model = Message
