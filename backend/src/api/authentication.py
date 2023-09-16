from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import get_current_active_user
from src.schemas import AuthUser, Token, User
from src.services.auth import AuthService
from src.services.user import UserService

router = APIRouter()


@router.post("/form_token")
async def form_login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthService = Depends(AuthService)
) -> Token:
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    return await auth_service.create_access_token(user.email)


@router.post("/token")
async def login_for_access_token(user: AuthUser, auth_service: AuthService = Depends(AuthService)) -> Token:
    user = await auth_service.authenticate_user(user.email, user.password)
    return await auth_service.create_access_token(user.email)


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@router.post("/users")
async def create_user(user: AuthUser, user_service: UserService = Depends(UserService)) -> User:
    return await user_service.create(user)


@router.post("/users/activate_user/{email}/{user_uuid}")
async def activate_user(email: str, user_uuid: UUID, auth_service: AuthService = Depends(AuthService)):
    await auth_service.activate_user(email, user_uuid)


@router.post("/users/prepare_restore_password")
async def prepare_restore_password(user: AuthUser, auth_service: AuthService = Depends(AuthService)):
    await auth_service.prepare_restore_password(user.email)


@router.post("/users/restore_password/{email}/{user_uuid}")
async def restore_password(
    email: str, user_uuid: UUID, password: AuthUser, auth_service: AuthService = Depends(AuthService)
):
    await auth_service.restore_password(email, user_uuid, password.password)
