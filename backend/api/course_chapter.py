from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlmodel.ext.asyncio.session import AsyncSession

from auth import get_current_active_user
from db.config import get_session
from db.models import Message, Theme, User
from db.services.chat import ChatService
from db.services.course_chapter import CourseChapterService

router = APIRouter()


@router.get("/{id}/themes/")
async def get_themes(id: int, session: AsyncSession = Depends(get_session)) -> List[Theme]:
    return await CourseChapterService(session).themes(id)


@router.get("/{id}/messages/", response_model=Page[Message])
async def get_messages(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
) -> List[Message]:
    service = ChatService(session)
    chat = await service.get_from_user_and_chapter(user_id=current_user.id, course_chapter_id=id)
    return paginate(await service.messages(chat.id))
