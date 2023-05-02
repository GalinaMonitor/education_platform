from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.auth import get_current_active_user
from backend.db.config import get_session
from backend.db.services.chat import ChatService
from backend.db.services.course_chapter import CourseChapterService
from backend.models import Message, ThemeVideos, User

router = APIRouter()


@router.get("/{id}/themes")
async def get_themes(id: int, session: AsyncSession = Depends(get_session)) -> List[ThemeVideos]:
    return await CourseChapterService(session).themes(id)


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
    service = ChatService(session)
    chat = await service.get_from_user_and_chapter(user_id=current_user.id, coursechapter_id=id)
    return await service.messages(chat.id, before=before, after=after, limit=limit, theme=theme)
