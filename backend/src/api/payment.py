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


async def get_body(request: Request):
    content_type = request.headers.get("Content-Type")
    if content_type is None:
        raise HTTPException(status_code=400, detail="No Content-Type provided!")
    elif content_type == "application/json":
        try:
            return await request.json()
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON data")
    elif content_type == "application/x-www-form-urlencoded" or content_type.startswith("multipart/form-data"):
        try:
            return await request.form()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Form data")
    else:
        raise HTTPException(status_code=400, detail="Content-Type not supported!")


@router.post("/lifepay_callback/")
async def lifepay_callback(
    data=Depends(get_body),
    payment_service: PaymentService = Depends(),
    user_service: UserService = Depends(),
):
    pprint(data.__dict__)
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
