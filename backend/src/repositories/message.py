from src.db.models import Message
from src.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
    model = Message
