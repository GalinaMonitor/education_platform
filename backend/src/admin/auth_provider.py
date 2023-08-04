from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from src.db.config import engine
from src.exceptions import UnauthorizedException


class MyAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        async_session = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
        async with async_session() as session:
            user = await authenticate_user(session, username, password)
        if not user or not user.is_admin:
            raise LoginFailed("Invalid username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        request.session.update({"access_token": access_token})
        return response

    async def is_authenticated(self, request) -> bool:
        if request.session.get("access_token", None):
            try:
                user = await get_current_user(request.session.get("access_token"))
            except UnauthorizedException:
                return False
            request.state.user = {
                "name": user.fullname,
                "avatar": user.avatar,
                "roles": ["read", "create", "edit", "delete", "action_make_published"],
            }
            return True
        return False

    def get_admin_user(self, request: Request) -> AdminUser:
        if hasattr(request.state, "user"):
            user = request.state.user
            return AdminUser(username=user["name"], photo_url=user["avatar"])
        return None

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
