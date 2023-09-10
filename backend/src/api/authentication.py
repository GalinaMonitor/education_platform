from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    prepare_activate_user,
)
from src.db.config import get_session
from src.db.services.user import UserService
from src.exceptions import AlreadyRegisteredException, UnauthorizedException
from src.models import AuthUser, User
from src.utils import init_user

router = APIRouter()


@router.post("/form_token")
async def form_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token")
async def login_for_access_token(user: AuthUser, session: AsyncSession = Depends(get_session)) -> Token:
    user = await authenticate_user(session, user.email, user.password)
    if not user:
        raise UnauthorizedException
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@router.post("/users")
async def create_user(user: AuthUser, session: AsyncSession = Depends(get_session)) -> User:
    try:
        user = await UserService(session).create(user)
    except IntegrityError:
        raise AlreadyRegisteredException
    await init_user(user)
    await prepare_activate_user(user.email)
    return user


@router.post("/users/activate_user/{email}/{user_uuid}")
async def activate_user(email: str, user_uuid: UUID):
    import src.auth as auth

    await auth.activate_user(email, user_uuid)


@router.post("/users/prepare_restore_password")
async def prepare_restore_password(user: AuthUser):
    import src.auth as auth

    await auth.prepare_restore_password(user.email)


@router.post("/users/restore_password/{email}/{user_uuid}")
async def restore_password(email: str, user_uuid: UUID, password: AuthUser):
    import src.auth as auth

    await auth.restore_password(email, user_uuid, password.password)
