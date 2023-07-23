from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from auth import get_current_active_user
from db.config import get_session
from db.models import SubscriptionType
from db.services.chat import ChatService
from db.services.course_chapter import CourseChapterService
from db.services.message import MessageService
from exceptions import HasNoSubscriptionException
from models import CourseChapterRead, Message, ThemeRead, User

router = APIRouter()


@router.get("/{id}/themes")
async def get_themes(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> List[ThemeRead]:
    return await CourseChapterService(session).themes(id=id, user_id=current_user.id)


@router.get("/{id}")
async def get_course_chapter(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> CourseChapterRead:
    return await CourseChapterService(session).retrieve_from_user_and_id(id=id, user_id=current_user.id)


@router.get("/{id}/messages", response_model=List[Message])
async def get_messages(
    id: int,
    before: Optional[int] = None,
    after: Optional[int] = None,
    limit: Optional[int] = None,
    theme: Optional[str] = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    session: AsyncSession = Depends(get_session),
) -> List[Message]:
    chat_service = ChatService(session)
    message_service = MessageService(session)
    chat = await chat_service.get_or_create_from_user_and_chapter(user_id=current_user.id, coursechapter_id=id)
    messages = await chat_service.messages(chat.id, before=before, after=after, limit=limit, theme=theme)
    for message in messages:
        await message_service.update(message.id, data=Message(is_read=True))
    return messages


@router.post("/{id}/activate")
async def activate_course_chapter(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    session: AsyncSession = Depends(get_session),
):
    if current_user.subscription_type == SubscriptionType.NO_SUBSCRIPTION:
        raise HasNoSubscriptionException
    service = ChatService(session)
    course_chapter = await CourseChapterService(session).retrieve(id=id)
    chat = await service.get_or_create_from_user_and_chapter(user_id=current_user.id, coursechapter_id=id)
    all_chats = await service.get_from_user_and_course(user_id=current_user.id, course_id=course_chapter.course_id)
    for deactivate_chat in all_chats:
        await service.deactivate(id=deactivate_chat.id)
    return await service.activate(id=chat.id)
