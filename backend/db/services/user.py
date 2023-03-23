from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException
from db.models import User, Chat
from db.services.base import BaseService
from models import CreateUser


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User

    async def create(self, data: CreateUser) -> User:
        from auth import pwd_context

        new_model = User(
            email=data.email,
            hashed_password=pwd_context.hash(data.password)
        )
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
