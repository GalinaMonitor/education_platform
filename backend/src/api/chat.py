from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate

from src.schemas import Message
from src.services.chat import ChatService

router = APIRouter()


@router.get("/{id}/messages")
async def get_messages(
    id: int, chat_service: ChatService = Depends(ChatService)
) -> Page[Message]:
    return paginate(await chat_service.messages(id))
