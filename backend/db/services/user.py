from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.models import Chat as ChatDB
from db.models import User as UserDB
from db.services.base import BaseService
from exceptions import NotFoundException
from models import AuthUser, Chat, ChatMessages, User


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = UserDB
        self.pydantic_model = User

    async def create(self, data: AuthUser) -> User:
        from auth import pwd_context

        date = datetime.now().date()
        password = data.password
        new_model = self.model(
            email=data.email,
            hashed_password=pwd_context.hash(password),
            has_subscription=True,
            end_of_subscription=date + timedelta(days=60),
        )
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
        statement = select(func.max(self.model.id).label("receive_time"))
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        return result
