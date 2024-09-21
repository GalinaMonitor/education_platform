from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile
from fastapi_pagination import Page, paginate

from src.auth import get_current_active_user
from src.s3.api import AWSClient
from src.schemas import Message, UpdateUser, User
from src.services.chat import ChatService
from src.services.user import UserService
from src.settings import settings

router = APIRouter()


@router.get("/total_users")
async def get_total_users(user_service: UserService = Depends(UserService)) -> int:
    return await user_service.get_total_users()


@router.get("/messages")
async def get_messages(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_service: UserService = Depends(UserService),
    chat_service: ChatService = Depends(ChatService),
) -> Page[Message]:
    chat = await user_service.get_base_chat(id=current_user.id)
    return paginate(await chat_service.messages(chat.id))


@router.patch("")
async def patch(
    user: UpdateUser,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_service: UserService = Depends(UserService),
) -> User:
    return await user_service.update(id=current_user.id, data=user)


@router.post("/avatar")
async def update_avatar(
    photo: UploadFile,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_service: UserService = Depends(UserService),
    aws_client: AWSClient = Depends(AWSClient),
) -> str:
    file_format = photo.filename.split(".")[-1]
    filename = f"{current_user.email}-{uuid4()}.{file_format}"
    aws_client.delete_file(filename)
    aws_client.upload_file(photo.file, filename)
    await user_service.update(
        id=current_user.id,
        data=UpdateUser(
            avatar=f"{settings.aws_host}/{settings.aws_bucket_name}/{filename}"
        ),
    )
    return f"{settings.aws_host}/{settings.aws_bucket_name}/{filename}"
