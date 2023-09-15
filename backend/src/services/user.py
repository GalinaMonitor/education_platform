import uuid
from datetime import datetime, timedelta

from src.exceptions import HasNoSubscriptionException
from src.repositories.user import UserRepository
from src.schemas import (
    AuthUser,
    Chat,
    ChatMessages,
    DataType,
    Message,
    SubscriptionType,
    User,
)
from src.services.base import BaseService
from src.services.chat import ChatService
from src.services.course_chapter import CourseChapterService
from src.services.mail import MailService
from src.services.message import MessageService
from src.text_constants import INIT_MESSAGE_INSTRUCTION, INIT_MESSAGE_WELCOME


class UserService(BaseService):
    model = User

    def __init__(self):
        super().__init__()
        self.repo = UserRepository()

    async def create(self, data: AuthUser) -> User:
        from src.auth import pwd_context

        raw_user = self.repo.create(
            {
                "email": data.email,
                "hashed_password": pwd_context.hash(data.password),
                "subscription_type": SubscriptionType.DEMO,
                "end_of_subscription": datetime.now().date() + timedelta(days=28),
            }
        )
        user = self.model.model_validate(raw_user)
        await self.init_user(user)
        await self.prepare_activate_user(user)
        return user

    async def prepare_activate_user(self, user: User) -> None:
        user_uuid = uuid.uuid4()
        await self.repo.update(user.id, {"service_uuid": user_uuid})
        await MailService().send_prepare_activate_email(user.email, user.service_uuid)

    async def init_user(self, user: User) -> None:
        chat = await ChatService().create(
            Chat(
                user_id=user.id,
            )
        )
        message_service = MessageService()
        await message_service.create(
            Message(
                datetime=datetime.now(),
                content=INIT_MESSAGE_WELCOME,
                content_type=DataType.TEXT,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        await message_service.create(
            Message(
                datetime=datetime.now(),
                content=INIT_MESSAGE_INSTRUCTION,
                content_type=DataType.TEXT,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        course_chapters = await CourseChapterService().list()
        chat_service = ChatService()
        for course_chapter in course_chapters:
            await chat_service.create(ChatMessages(user_id=user.id, coursechapter_id=course_chapter.id))

    async def get_by_email(self, email: str) -> User:
        return self.model.model_validate(await self.repo.get_by_email(email))

    async def get_base_chat(self, id: int) -> Chat:
        return Chat.model_validate(await self.repo.get_base_chat(id))

    async def get_total_users(self) -> int:
        return await self.repo.get_total_users()

    async def check_subscription(self, user: User) -> None:
        if user.subscription_type == SubscriptionType.NO_SUBSCRIPTION:
            raise HasNoSubscriptionException
