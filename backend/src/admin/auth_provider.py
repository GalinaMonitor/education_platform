from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider

from src.db.config import get_session_context
from src.exceptions import UnauthorizedException
from src.repositories.user import UserRepository
from src.services.user import UserService


class MyAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        from src.services.auth import AuthService

        async with get_session_context() as session:
            auth_service = AuthService(
                repo=UserRepository(session),
                user_service=UserService(UserRepository(session)),
            )
            user = await auth_service.authenticate_admin(username, password)
            token = await auth_service.create_access_token(user.email)
            request.session.update(token.model_dump())
        return response

    async def is_authenticated(self, request: Request) -> bool:
        from src.auth import get_current_user

        if request.session.get("access_token", None):
            try:
                async with get_session_context() as session:
                    user = await get_current_user(
                        token=request.session.get("access_token"),
                        user_service=UserService(UserRepository(session)),
                    )
            except UnauthorizedException:
                return False
            request.state.user = {
                "name": user.fullname,
                "avatar": user.avatar,
                "roles": ["read", "create", "edit", "delete", "action_make_published"],
            }
            return True
        return False

    def get_admin_user(self, request: Request) -> AdminUser | None:
        if hasattr(request.state, "user"):
            user = request.state.user
            return AdminUser(username=user["name"], photo_url=user["avatar"])
        return None

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
