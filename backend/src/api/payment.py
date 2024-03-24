import json
from json import JSONDecodeError
from pprint import pprint
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import AnyUrl, Json
from starlette.requests import Request

from src.auth import get_current_active_user
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


async def get_data(request: Request):
    try:
        form = await request.form()
        return json.loads(dict(form)["data"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Form data")


@router.post("/lifepay_callback/")
async def lifepay_callback(
    data=Depends(get_data),
    payment_service: PaymentService = Depends(),
    user_service: UserService = Depends(),
):
    pprint(data)
    data = LifePayCallbackData.model_validate(data)
    if data.status != "success":
        return
    user = await user_service.get_by_email(data.email)
    subscription_info = payment_service.get_subscription_info_from_cost(data.purchase.pop().amount)
    await user_service.update(
        user.id,
        UpdateUser(
            end_of_subscription=user.end_of_subscription + subscription_info.duration,
            subscription_type=SubscriptionType.LEARN_ALL,
        ),
    )
