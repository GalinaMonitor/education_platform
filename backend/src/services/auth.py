import uuid
from typing import Union

from fastapi import Depends

from src.auth import pwd_context, verify_password
from src.exceptions import UnauthorizedException
from src.repositories.user import UserRepository
from src.schemas import AuthUser, Token, User
from src.services.user import UserService


class AuthService:
    def __init__(
        self, repo: UserRepository = Depends(), user_service: UserService = Depends()
    ):
        self.repo = repo
        self.user_service = user_service

    async def authenticate_user(
        self, username: str, password: str
    ) -> Union[bool, User]:
        user = User.model_validate(await self.repo.get_by_email(username))
        if not verify_password(password, user.hashed_password) or not user.is_active:
            raise UnauthorizedException
        return user

    async def authenticate_admin(
        self, username: str, password: str
    ) -> Union[bool, User]:
        user = User.model_validate(await self.repo.get_by_email(username))
        if (
            not verify_password(password, user.hashed_password)
            or not user.is_active
            or not user.is_admin
        ):
            raise UnauthorizedException
        return user

    async def create_access_token(self, email: str) -> Token:
        from src import auth

        return auth.create_access_token(email)

    async def prepare_restore_password(self, email: str) -> None:
        from src.services.mail import MailService

        user_uuid = uuid.uuid4()
        user = await self.user_service.get_by_email(email)
        await self.repo.update(user.id, data={"service_uuid": user_uuid})
        await MailService().send_prepare_restore_password_email(email, user_uuid)

    async def restore_password(
        self, email: str, user_uuid: uuid.UUID, password: str
    ) -> None:
        user = await self.user_service.get_by_email(email)
        if user.service_uuid != user_uuid:
            raise UnauthorizedException
        await self.user_service.update(
            user.id, data=AuthUser(hashed_password=pwd_context.hash(password))
        )

    async def activate_user(self, email: str, user_uuid: uuid.UUID) -> None:
        user = await self.user_service.get_by_email(email)
        if user.service_uuid != user_uuid:
            raise UnauthorizedException
        await self.user_service.update(user.id, data=AuthUser(is_active=True))
