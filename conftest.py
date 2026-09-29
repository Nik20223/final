"""Фикстуры проекта: драйвер браузера, API-клиенты и скриншоты при падении."""

import os
from datetime import datetime

import pytest
import requests
from selenium.webdriver.support.ui import WebDriverWait

from api.api_client import ApiClient
from api.auth_api import AuthApi
from api.booking_api import BookingApi
from api.report_api import ReportApi
from api.room_api import RoomApi
from config import config
from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory

SCREENSHOTS_DIR = "screenshots"


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат каждой фазы теста в ``item.rep_*``."""
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report


@pytest.fixture()
def driver(request):
    """Поднимает WebDriver и сохраняет скриншот, если тест упал."""
    driver = DriverFactory.create()
    yield driver
    _take_screenshot(driver, request.node)
    driver.quit()


@pytest.fixture()
def admin(driver):
    """Логинит администратора и ждёт перехода в панель."""
    LoginPage(driver).open().login(
        config.ADMIN_USERNAME, config.ADMIN_PASSWORD
    )
    WebDriverWait(driver, config.DEFAULT_TIMEOUT).until(
        lambda d: "/admin/rooms" in d.current_url
    )
    return driver


@pytest.fixture()
def api_session():
    """Общая сессия, чтобы cookie токена разделялись между сервисами."""
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture()
def api_client(api_session):
    """Низкоуровневый HTTP-клиент сервиса Booking на общей сессии."""
    return ApiClient(config.BOOKING_API_URL, session=api_session)


@pytest.fixture()
def auth_api(api_session):
    """Клиент сервиса авторизации на общей сессии."""
    return AuthApi(session=api_session)


@pytest.fixture()
def booking_api(api_session):
    """Клиент сервиса Booking на общей сессии."""
    return BookingApi(session=api_session)


@pytest.fixture()
def room_api(api_session):
    """Клиент сервиса комнат на общей сессии."""
    return RoomApi(session=api_session)


@pytest.fixture()
def report_api(api_session):
    """Клиент сервиса отчётов на общей сессии."""
    return ReportApi(session=api_session)


def _take_screenshot(driver, node):
    """Сохраняет скриншот упавшего теста в ``screenshots/``."""
    report = getattr(node, "rep_call", None)
    if report is None or not report.failed:
        return

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOTS_DIR, f"{node.name}_{stamp}.png")
    driver.save_screenshot(path)

    try:
        import allure
    except ImportError:
        return
    allure.attach.file(
        path,
        name="screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
