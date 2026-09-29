"""UI-тесты авторизации в админ-панели."""

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from config import config
from pages.login_page import LoginPage
from pages.room_page import RoomPage

pytestmark = pytest.mark.ui


@allure.feature("Авторизация (UI)")
class TestLoginUi:
    """Вход в админ-панель и выход из неё."""

    @allure.title("Вход с валидными данными открывает панель")
    def test_login_with_valid_credentials(self, admin):
        assert "/admin/rooms" in admin.current_url

    @allure.title("Неверный пароль показывает ошибку")
    def test_login_with_invalid_credentials(self, driver):
        page = LoginPage(driver).open().login(
            config.ADMIN_USERNAME, "wrong-password"
        )
        assert page.is_error_displayed()

    @allure.title("Выход покидает админ-панель")
    def test_logout_leaves_admin_panel(self, admin):
        RoomPage(admin).logout()

        WebDriverWait(admin, config.DEFAULT_TIMEOUT).until(
            lambda d: "/admin" not in d.current_url
        )
        assert "/admin" not in admin.current_url
