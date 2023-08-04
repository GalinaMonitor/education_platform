from typing import List

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.config import get_session
from src.db.services.chat import ChatService
from src.models import Message

router = APIRouter()


@router.get("/{id}/messages", response_model=Page[Message])
async def get_messages(id: int, session: AsyncSession = Depends(get_session)) -> List[Message]:
    return paginate(await ChatService(session).messages(id))
