from uuid import UUID

from fastapi_mail import FastMail, MessageSchema, MessageType

from src.main import email_conf
from src.settings import settings
from src.text_constants import (
    EMAIL_ACTIVATE_ACCOUNT,
    EMAIL_NEW_VIDEO,
    EMAIL_RESTORE_PASSWORD,
)


class MailService:
    async def send_prepare_activate_email(self, email: str, user_uuid: UUID):
        message = MessageSchema(
            subject=EMAIL_ACTIVATE_ACCOUNT,
            recipients=[email],
            template_body={"url": f"{settings.front_url}/activate_user/{email}/{user_uuid}"},
            subtype=MessageType.html,
        )
        fm = FastMail(email_conf)
        await fm.send_message(message, template_name="activate_user.html")

    async def send_prepare_restore_password_email(self, email, user_uuid: UUID):
        message = MessageSchema(
            subject=EMAIL_RESTORE_PASSWORD,
            recipients=[email],
            template_body={"url": f"{settings.front_url}/restore_password/{email}/{user_uuid}"},
            subtype=MessageType.html,
        )
        fm = FastMail(email_conf)
        await fm.send_message(message, template_name="restore_password.html")

    async def send_new_video_email(self, email, coursechapter_name, video_name):
        message = MessageSchema(
            subject=EMAIL_NEW_VIDEO,
            recipients=[email],
            template_body={
                "url": f"{settings.front_url}",
                "coursechapter": coursechapter_name,
                "video": video_name,
            },
            subtype=MessageType.html,
        )
        fm = FastMail(email_conf)
        await fm.send_message(message, template_name="new_video.html")
