from typing import Annotated, List

from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate
from sqlmodel.ext.asyncio.session import AsyncSession

from auth import get_current_active_user
from db.config import get_session
from db.models import Message, User
from db.services.chat import ChatService
from db.services.user import UserService
from models import UpdateUser
from s3.api import AWSClient
from settings import settings

router = APIRouter()


@router.get("/messages/", response_model=Page[Message])
async def get_messages(
    current_user: Annotated[User, Depends(get_current_active_user)], session: AsyncSession = Depends(get_session)
) -> List[Message]:
    user_service = UserService(session)
    chat_service = ChatService(session)
    chat = await user_service.get_base_chat(id=current_user.id)
    return paginate(await chat_service.messages(chat.id))


@router.patch("/")
async def patch(
    user: UpdateUser,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).update(id=current_user.id, data=user)


@router.post("/avatar/")
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
        id=current_user.id, data=UpdateUser(avatar=f"https://s3.timeweb.com/2d09b0cd-education_platform/{filename}")
    )
    return f"{settings.aws_host}/{settings.aws_bucket_name}/{filename}"
