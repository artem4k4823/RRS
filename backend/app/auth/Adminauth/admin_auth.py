
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi import HTTPException, status
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware



class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail = "Неверный логин или пароль")
        request.session.update({"token": settings.SECRET_KEY})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
