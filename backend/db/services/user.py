import secrets

from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException
from db.models import Chat, User
from db.services.base import BaseService
from models import CreateUser


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User

    async def create(self, data: CreateUser) -> User:
        from auth import pwd_context
        from main import email_conf

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
        new_model = User(email=data.email, hashed_password=pwd_context.hash(password))
        self.session.add(new_model)
        await self.session.commit()
        return new_model

    async def get_by_email(self, email: str) -> User:
        statement = select(self.model).where(self.model.email == email)
        results = await self.session.exec(statement)
        result = results.first()
        if not result:
            raise NotFoundException()
        return result

    async def get_base_chat(self, id: int) -> Chat:
        statement = select(Chat).where(Chat.user_id == id and Chat.coursechapter_id is None)
        results = await self.session.exec(statement)
        result = results.first()
        if not result:
            raise NotFoundException()
        return result
