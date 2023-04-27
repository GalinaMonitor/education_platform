import secrets

from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.db.exceptions import NotFoundException
from backend.db.models import Chat as ChatDB
from backend.db.models import User as UserDB
from backend.db.services.base import BaseService
from backend.models import Chat, ChatMessages, CreateUser, User


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = UserDB
        self.pydantic_model = User

    async def create(self, data: CreateUser) -> User:
        from backend.auth import pwd_context
        from backend.main import email_conf

        if not data.password:
            password = secrets.token_urlsafe(32)
            message = MessageSchema(
                subject="Registration",
                recipients=[data.email],
                body=f"Here is your password {password}",
                subtype=MessageType.plain,
            )
            fm = FastMail(email_conf)
            await fm.send_message(message)
        else:
            password = data.password
        new_model = UserDB(email=data.email, hashed_password=pwd_context.hash(password))
        self.session.add(new_model)
        await self.session.commit()
        return self.pydantic_model.from_orm(new_model)

    async def get_by_email(self, email: str) -> User:
        statement = select(self.model).where(self.model.email == email)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return self.pydantic_model.from_orm(result)

    async def get_base_chat(self, id: int) -> ChatMessages:
        statement = select(ChatDB).where(
            ChatDB.user_id == id, ChatDB.coursechapter_id == None
        )
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return Chat.from_orm(result)
