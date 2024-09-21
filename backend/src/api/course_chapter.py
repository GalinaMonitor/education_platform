from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from src.auth import get_current_active_user
from src.schemas import CourseChapterRead, Message, PaginationParams, ThemeRead, User
from src.services.chat import ChatService
from src.services.course_chapter import CourseChapterService
from src.services.message import MessageService
from src.services.user import UserService

router = APIRouter()


@router.get("/{id}/themes")
async def get_themes(
    id: int,
    coursechapter_service: CourseChapterService = Depends(CourseChapterService),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> List[ThemeRead]:
    return await coursechapter_service.themes(id=id, user_id=current_user.id)


@router.get("/{id}")
async def get_course_chapter(
    id: int,
    coursechapter_service: CourseChapterService = Depends(CourseChapterService),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> CourseChapterRead:
    return await coursechapter_service.retrieve_from_user_and_id(
        id=id, user_id=current_user.id
    )


@router.get("/{id}/messages", response_model=List[Message])
async def get_messages(
    id: int,
    theme_id: Optional[str] = None,
    pagination_params: PaginationParams = Depends(PaginationParams),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    chat_service: ChatService = Depends(ChatService),
    message_service: MessageService = Depends(MessageService),
) -> List[Message]:
    chat = await chat_service.get_or_create_from_user_and_chapter(
        user_id=current_user.id, coursechapter_id=id
    )
    messages = await chat_service.messages(
        chat.id, pagination_params, theme_id=theme_id
    )
    await message_service.update_all(
        [m.id for m in messages], data=Message(is_read=True)
    )
    return messages


@router.post("/{id}/activate")
async def activate_course_chapter(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    chat_service: ChatService = Depends(ChatService),
    coursechapter_service: CourseChapterService = Depends(CourseChapterService),
    user_service: UserService = Depends(UserService),
) -> None:
    await user_service.check_subscription(current_user)
    coursechapter = await coursechapter_service.retrieve(id=id)
    chat = await chat_service.get_or_create_from_user_and_chapter(
        user_id=current_user.id, coursechapter_id=id
    )
    await chat_service.activate(chat, current_user, coursechapter)
