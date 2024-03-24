from datetime import timedelta
from urllib.parse import urljoin

import httpx

from src.schemas import BaseModel, PaymentData, SubscriptionLength
from src.settings import settings

SUBSCRIPTION_PARAMS = {
    SubscriptionLength.MONTH: {
        "description": "Месячная подписка на Ку-Помогу",
        "amount": 10,
        "duration": timedelta(days=30),
    },
    SubscriptionLength.QUARTER: {
        "description": "Квартальная подписка на Ку-Помогу",
        "amount": 20,
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
        async with httpx.AsyncClient(base_url="https://api.life-pay.ru/v1/") as client:
            response = await client.post(url="bill", json=request_data)
        return PaymentData.model_validate(response.json()["data"])

    def get_subscription_info_from_cost(self, amount: int):
        for subscription_info in SUBSCRIPTION_PARAMS.values():
            if subscription_info["amount"] == amount:
                return SubscriptionSchema(
                    duration=subscription_info["duration"],
                    amount=subscription_info["amount"],
                    description=subscription_info["description"],
                )
