from datetime import timedelta
from typing import Annotated

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
from db.services.user import UserService
from exceptions import AlreadyRegisteredException, UnauthorizedException
from models import AuthUser, User
from utils import init_user

router = APIRouter()


@router.post("/form_token", response_model=Token)
async def form_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(user: AuthUser, session: AsyncSession = Depends(get_session)):
    dwedwe
    user = await authenticate_user(session, user.email, user.password)
    if not user:
        raise UnauthorizedException
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
        raise AlreadyRegisteredException
    await init_user(user)
    return user
