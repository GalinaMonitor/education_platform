from datetime import datetime, timedelta
from typing import Annotated

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from db.config import get_session
from db.models import Message
from db.services.chat import ChatService
from db.services.course_chapter import CourseChapterService
from db.services.message import MessageService
from db.services.user import UserService
from models import AuthUser, ChatMessages, User
from utils import init_user

router = APIRouter()


@router.post("/form_token", response_model=Token)
async def form_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(user: AuthUser, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/users", response_model=User)
async def create_user(user: AuthUser, session: AsyncSession = Depends(get_session)):
    try:
        user = await UserService(session).create(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )
    await init_user(user)
    return user
