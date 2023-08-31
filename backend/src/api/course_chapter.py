from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth import get_current_active_user
from src.db.config import get_session
from src.db.models import DataType, SubscriptionType
from src.db.services.chat import ChatService
from src.db.services.course_chapter import CourseChapterService
from src.db.services.message import MessageService
from src.exceptions import HasNoSubscriptionException
from src.models import CourseChapterRead, Message, ThemeRead, UpdateChat, User

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
    if not chat.get_welcome_message:
        await MessageService(session).create(
            Message(
                datetime=datetime.now(),
                content=f"Ку, {current_user.fullname}! " + course_chapter.welcome_message
                if current_user.fullname
                else "Ку! " + course_chapter.welcome_message,
                content_type=DataType.TEXT,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        await service.update(id=chat.id, data=UpdateChat(get_welcome_message=True))
    all_chats = await service.get_from_user_and_course(user_id=current_user.id, course_id=course_chapter.course_id)
    for deactivate_chat in all_chats:
        await service.deactivate(id=deactivate_chat.id)
    return await service.activate(id=chat.id)
