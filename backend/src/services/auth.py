import uuid
from typing import Union

from src.auth import pwd_context, verify_password
from src.exceptions import UnauthorizedException
from src.repositories.user import UserRepository
from src.schemas import AuthUser, Token, User


class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    async def authenticate_user(self, username: str, password: str) -> Union[bool, User]:
        user = User.model_validate(await self.repo.get_by_email(username))
        if not verify_password(password, user.hashed_password) or not user.is_active:
            raise UnauthorizedException
        return user

    async def authenticate_admin(self, username: str, password: str) -> Union[bool, User]:
        user = User.model_validate(await self.repo.get_by_email(username))
        if not verify_password(password, user.hashed_password) or not user.is_active or not user.is_admin:
            raise UnauthorizedException
        return user

    async def create_access_token(self, email: str) -> Token:
        from src import auth

        return auth.create_access_token(email)

    async def prepare_restore_password(self, email: str) -> None:
        from src.services.mail import MailService
        from src.services.user import UserService

        user_uuid = uuid.uuid4()
        user = await UserService().get_by_email(email)
        await self.repo.update(user.id, data={"service_uuid": user_uuid})
        await MailService().send_prepare_restore_password_email(email, user_uuid)

    async def restore_password(self, email: str, user_uuid: uuid.UUID, password: str) -> None:
        from src.services.user import UserService

        user = await UserService().get_by_email(email)
        if user.service_uuid != user_uuid:
            raise UnauthorizedException
        await UserService().update(user.id, data=AuthUser(hashed_password=pwd_context.hash(password)))

    async def activate_user(self, email: str, user_uuid: uuid.UUID) -> None:
        from src.services.user import UserService

        user = await UserService().get_by_email(email)
        if user.service_uuid != user_uuid:
            raise UnauthorizedException
        await UserService().update(user.id, data=AuthUser(is_active=True))
