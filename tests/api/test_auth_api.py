"""API-тесты сервиса авторизации."""

import allure
import pytest

from api.auth_api import AuthError
from config import config

pytestmark = pytest.mark.api


@allure.feature("Auth API")
class TestAuthApi:
    """Проверки /auth/login, /auth/validate и /auth/logout."""

    @allure.title("Логин возвращает токен")
    def test_login_returns_token(self, auth_api):
        assert auth_api.login()

    @allure.title("Неверный пароль даёт 403")
    def test_login_with_wrong_password(self, auth_api):
        with pytest.raises(AuthError) as excinfo:
            auth_api.login(config.ADMIN_USERNAME, "wrong-password")
        assert excinfo.value.status_code == 403

    @allure.title("Свежий токен проходит валидацию")
    def test_validate_accepts_fresh_token(self, auth_api):
        token = auth_api.login()
        assert auth_api.validate(token) is True

    @allure.title("Неизвестный токен не проходит валидацию")
    def test_validate_rejects_unknown_token(self, auth_api):
        assert auth_api.validate("not-a-real-token") is False

    @allure.title("Logout инвалидирует токен")
    def test_logout_invalidates_token(self, auth_api):
        token = auth_api.login()
        assert auth_api.logout(token) is True
        assert auth_api.validate(token) is False
