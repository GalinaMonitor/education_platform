import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.background import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema, MessageType
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.config import engine
from db.models import User
from db.services.user import UserService
from exceptions import UnauthorizedException
from models import AuthUser
from settings import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 4320


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/form_token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(session, username: str, password: str):
    user = await UserService(session).get_by_email(username)
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedException
    except JWTError:
        raise UnauthorizedException
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        user = await UserService(session).get_by_email(username)
    if user is None:
        raise UnauthorizedException
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


async def prepare_restore_password(email):
    from main import email_conf

    user_uuid = uuid.uuid4()
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        user = await UserService(session).get_by_email(email)
        await UserService(session).update(user.id, data=AuthUser(service_uuid=user_uuid))
    message = MessageSchema(
        subject="Восстановление пароля",
        recipients=[email],
        body=f"Для восстановления пароля перейдите по "
        f"<a href='{settings.front_url}/restore_password/{email}/{user_uuid}'>ссылке</a>",
        subtype=MessageType.html,
    )
    # background_tasks = BackgroundTasks()
    fm = FastMail(email_conf)
    await fm.send_message(message, template_name=None)
    # background_tasks.add_task(fm.send_message, message, template_name=None)


async def restore_password(email, user_uuid, password):
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        user = await UserService(session).get_by_email(email)
        if user.service_uuid != user_uuid:
            raise UnauthorizedException
        await UserService(session).update(user.id, data=AuthUser(hashed_password=pwd_context.hash(password)))
