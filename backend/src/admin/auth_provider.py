from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider

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
        from src.services.auth import AuthService

        user = await AuthService().authenticate_admin(username, password)
        request.session.update({"access_token": AuthService().create_access_token(user.email)})
        return response

    async def is_authenticated(self, request: Request) -> bool:
        from src.auth import get_current_user

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

    def get_admin_user(self, request: Request) -> AdminUser | None:
        if hasattr(request.state, "user"):
            user = request.state.user
            return AdminUser(username=user["name"], photo_url=user["avatar"])
        return None

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
