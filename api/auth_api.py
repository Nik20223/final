"""Хелперы для сервиса авторизации Restful Booker Platform."""

from api.api_client import ApiClient
from config import config

TOKEN_COOKIE = "token"


class AuthError(Exception):
    """Ошибка авторизации, хранит HTTP-статус ответа сервиса."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class AuthApi:
    """Эндпоинты сервиса auth: /login, /validate, /logout."""

    def __init__(self, base_url=None, session=None, timeout=None):
        """Клиент сервиса auth; сессию можно разделить с другими API."""
        self.client = ApiClient(
            base_url or config.AUTH_API_URL,
            session=session,
            timeout=timeout,
        )

    def login(self, username=None, password=None):
        """Авторизоваться и вернуть токен из cookie сервиса."""
        payload = {
            "username": username or config.ADMIN_USERNAME,
            "password": password or config.ADMIN_PASSWORD,
        }
        response = self.client.post("/login", json=payload)
        if response.status_code != 200:
            raise AuthError(
                f"Авторизация не удалась: HTTP {response.status_code}",
                status_code=response.status_code,
            )

        token = self.client.session.cookies.get(TOKEN_COOKIE)
        if not token:
            raise AuthError("Сервис не вернул cookie token")
        return token

    def validate(self, token):
        """Проверить токен: ``True``, если сервис считает его валидным."""
        response = self.client.post(
            "/validate", json={TOKEN_COOKIE: token}
        )
        return response.status_code == 200

    def logout(self, token):
        """Инвалидировать токен: ``True``, если сервис его удалил."""
        response = self.client.post(
            "/logout", json={TOKEN_COOKIE: token}
        )
        return response.status_code == 200
