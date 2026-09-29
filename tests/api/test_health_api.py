"""Тесты доступности (health) сервисов платформы."""

import allure
import pytest

from api.api_client import ApiClient
from config import config

pytestmark = [pytest.mark.api, pytest.mark.smoke]

SERVICES = [
    config.BOOKING_API_URL,
    config.ROOM_API_URL,
    config.AUTH_API_URL,
    config.BRANDING_API_URL,
    config.REPORT_API_URL,
    config.MESSAGE_API_URL,
]


@allure.feature("Health")
class TestHealthApi:
    """Каждый сервис отвечает статусом UP на /actuator/health."""

    @allure.title("Сервис доступен и отвечает UP")
    @pytest.mark.parametrize("base_url", SERVICES)
    def test_service_is_up(self, base_url):
        client = ApiClient(base_url)
        try:
            response = client.get("/actuator/health")
        finally:
            client.close()

        assert response.status_code == 200
        assert response.json()["status"] == "UP"
