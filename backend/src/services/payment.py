from datetime import timedelta
from urllib.parse import urljoin

import httpx

from src.exceptions import PaymentException
from src.schemas import (
    BaseModel,
    LifePayCallbackPurchase,
    PaymentData,
    SubscriptionLength,
)
from src.settings import settings

SUBSCRIPTION_PARAMS = {
    SubscriptionLength.MONTH: {
        "description": "Месячная подписка на Ку-Помогу",
        "amount": 3599,
        "duration": timedelta(days=30),
    },
    SubscriptionLength.QUARTER: {
        "description": "Квартальная подписка на Ку-Помогу",
        "amount": 7899,
        "duration": timedelta(days=120),
    },
}


class SubscriptionSchema(BaseModel):
    description: str
    amount: int
    duration: timedelta


class PaymentService:
    async def get_payment_data(self, subscription_length: SubscriptionLength, user_email: str) -> PaymentData:
        from src.main import app

        subscription_params = SUBSCRIPTION_PARAMS[subscription_length]
        request_data = {
            "apikey": settings.lifepay_api_key,
            "login": settings.lifepay_login,
            "amount": str(subscription_params["amount"]),
            "description": subscription_params["description"],
            "customer_email": user_email,
        }
        if not settings.debug:
            request_data["callback_url"] = urljoin(settings.service_url, app.url_path_for("lifepay_callback"))
        try:
            async with httpx.AsyncClient(base_url="https://api.life-pay.ru/v1/") as client:
                response = await client.post(url="bill", json=request_data)
            return PaymentData.model_validate(response.json()["data"])
        except Exception:
            raise PaymentException

    def get_subscription_info_from_cost(self, purchase_data: LifePayCallbackPurchase):
        for subscription_info in SUBSCRIPTION_PARAMS.values():
            if (
                subscription_info["amount"] == purchase_data.amount
                and subscription_info["description"] == purchase_data.name
            ):
                return SubscriptionSchema(
                    duration=subscription_info["duration"],
                    amount=subscription_info["amount"],
                    description=subscription_info["description"],
                )
