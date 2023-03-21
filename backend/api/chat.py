from typing import List

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate

from db.config import get_session
from db.models.all_models import Message
from sqlmodel.ext.asyncio.session import AsyncSession

from db.services.chat import ChatService

router = APIRouter()


@router.get('/{id}', response_model=Page[Message])
async def get_messages(id: int, session: AsyncSession = Depends(get_session)) -> List[Message]:
    return paginate(await ChatService(session).messages(id))
