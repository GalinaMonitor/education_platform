import secrets

from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException
from db.models import Chat as ChatDB
from db.models import User as UserDB
from db.services.base import BaseService
from models import AuthUser, Chat, ChatMessages, User


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = UserDB
        self.pydantic_model = User

    async def create(self, data: AuthUser) -> User:
        from auth import pwd_context

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
        statement = select(ChatDB).where(ChatDB.user_id == id, ChatDB.coursechapter_id == None)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return Chat.from_orm(result)

    async def get_total_users(self) -> int:
        statement = select(func.max(UserDB.id).label("receive_time"))
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        return result
