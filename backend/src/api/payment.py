import json
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import AnyUrl
from starlette.requests import Request

from src.auth import get_current_active_user
from src.logging_config import logger
from src.schemas import (
    LifePayCallbackData,
    SubscriptionLength,
    SubscriptionType,
    UpdateUser,
    User,
)
from src.services.payment import PaymentService
from src.services.user import UserService

router = APIRouter()


@router.post("/get_payment_link/{subscription_length}/")
async def get_payment_link(
    subscription_length: SubscriptionLength,
    payment_service: PaymentService = Depends(),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> AnyUrl:
    payment_data = await payment_service.get_payment_data(subscription_length, current_user.email)
    return payment_data.payment_url


async def get_data(request: Request) -> LifePayCallbackData:
    return LifePayCallbackData.model_validate(json.loads(dict(await request.form())["data"]))


@router.post("/lifepay_callback/")
async def lifepay_callback(
    data: LifePayCallbackData = Depends(get_data),
    payment_service: PaymentService = Depends(),
    user_service: UserService = Depends(),
):
    if data.status != "success":
        logger.warning(f"Payment error\n{data}")
        return
    user = await user_service.get_by_email(data.email)
    subscription_info = payment_service.get_subscription_info_from_cost(data.purchase.pop())
    if user.end_of_subscription and user.end_of_subscription >= datetime.now():
        end_of_subscription = user.end_of_subscription + subscription_info.duration
    else:
        end_of_subscription = datetime.now() + subscription_info.duration
    await user_service.update(
        user.id,
        UpdateUser(
            end_of_subscription=end_of_subscription,
            subscription_type=SubscriptionType.LEARN_ALL,
        ),
    )
