from typing import Annotated, List

from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth import get_current_active_user
from src.db.config import get_session
from src.db.services.chat import ChatService
from src.db.services.user import UserService
from src.models import Message, UpdateUser, User
from src.s3.api import AWSClient
from src.settings import settings

router = APIRouter()


@router.get("/total_users")
async def get_total_users(session: AsyncSession = Depends(get_session)):
    return await UserService(session).get_total_users()


@router.get("/messages", response_model=Page[Message])
async def get_messages(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
) -> List[Message]:
    user_service = UserService(session)
    chat_service = ChatService(session)
    chat = await user_service.get_base_chat(id=current_user.id)
    return paginate(await chat_service.messages(chat.id))


@router.patch("")
async def patch(
    user: UpdateUser,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).update(id=current_user.id, data=user)


@router.post("/avatar")
async def update_avatar(
    photo: UploadFile,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    file_format = photo.filename.split(".")[-1]
    filename = f"{current_user.fullname}.{file_format}"
    AWSClient().delete_file(filename)
    AWSClient().upload_file(photo.file, filename)
    await UserService(session).update(
        id=current_user.id,
        data=UpdateUser(avatar=f"{settings.aws_host}/{settings.aws_bucket_name}/{filename}"),
    )
    return f"{settings.aws_host}/{settings.aws_bucket_name}/{filename}"
