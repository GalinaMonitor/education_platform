from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

import models as pyd_models
from db import models as db_models
from db.models import SubscriptionType
from db.services.base import BaseService
from exceptions import NotFoundException


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.User
        self.pydantic_model = pyd_models.User

    async def create(self, data: pyd_models.AuthUser) -> pyd_models.User:
        from auth import pwd_context

        date = datetime.now().date()
        password = data.password
        new_model = self.model(
            email=data.email,
            hashed_password=pwd_context.hash(password),
            subscription_type=SubscriptionType.DEMO,
            end_of_subscription=date + timedelta(days=60),
        )
        self.session.add(new_model)
        await self.session.commit()
        return self.pydantic_model.from_orm(new_model)

    async def get_by_email(self, email: str) -> pyd_models.User:
        statement = select(self.model).where(self.model.email == email)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return self.pydantic_model.from_orm(result)

    async def get_base_chat(self, id: int) -> pyd_models.ChatMessages:
        statement = select(db_models.Chat).where(db_models.Chat.user_id == id, db_models.Chat.coursechapter_id == None)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return pyd_models.Chat.from_orm(result)

    async def get_total_users(self) -> int:
        statement = select(func.count(self.model.id))
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        return result
