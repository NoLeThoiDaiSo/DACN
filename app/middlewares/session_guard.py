from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.services.users import user_service
from app.utils.flash import set_flash

EXCLUDE_PREFIXES = ("/static", "/openapi.json", "/docs", "/redoc")

class SessionGuardMiddleware(BaseHTTPMiddleware):
    """
    Nếu session có 'user' nhưng user_service không còn user đó (RAM reset/xóa),
    thì xóa 'user' khỏi session và gắn flash 'Phiên đăng nhập đã hết hạn'.
    """

    async def dispatch(self, request: Request, call_next):
        # Chỉ xử lý HTTP, bỏ qua static/docs
        if request.scope.get("type") != "http":
            return await call_next(request)
        path = request.url.path
        if path.startswith(EXCLUDE_PREFIXES):
            return await call_next(request)

        # Nếu vì lý do gì đó SessionMiddleware chưa cài, đừng đụng request.session
        if "session" not in request.scope:
            return await call_next(request)

        username = request.session.get("user")
        if username and not user_service.exists(username):
            request.session.pop("user", None)
            set_flash(request, "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "info")

        response: Response = await call_next(request)
        return response
