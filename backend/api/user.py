from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate

from db.config import get_session
from db.models import Message, User
from sqlmodel.ext.asyncio.session import AsyncSession
from auth import get_current_active_user

from db.services.chat import ChatService
from db.services.user import UserService

router = APIRouter()


@router.get('/messages/', response_model=Page[Message])
async def get_messages(current_user: Annotated[User, Depends(get_current_active_user)],
                       session: AsyncSession = Depends(get_session)) -> List[Message]:
    user_service = UserService(session)
    chat_service = ChatService(session)
    chat = await user_service.get_base_chat(id=current_user.id)
    return paginate(await chat_service.messages(chat.id))
