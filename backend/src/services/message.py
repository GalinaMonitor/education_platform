from src.repositories.message import MessageRepository
from src.schemas import Message
from src.services.base import BaseService


class MessageService(BaseService):
    model = Message

    def __init__(self):
        super().__init__()
        self.repo = MessageRepository()
