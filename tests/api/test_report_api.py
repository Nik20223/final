"""API-тесты сервиса отчётов."""

import allure
import pytest

from utils.data_generator import booking_payload, future_dates

pytestmark = pytest.mark.api

ROOM_ID = 1


@pytest.fixture()
def login(auth_api):
    """Авторизует общую сессию под администратором."""
    return auth_api.login()


@pytest.fixture()
def booked_period(booking_api, login):
    """Бронирует комнату и убирает бронь после теста."""
    checkin, checkout = future_dates(start_in_days=90, nights=2)
    response = booking_api.create(
        booking_payload(ROOM_ID, checkin, checkout)
    )
    booking_id = response.json()["bookingid"]

    yield checkin, checkout
    booking_api.delete(booking_id)


@allure.feature("Report API")
class TestReportApi:
    """Отчёты по занятости комнат."""

    @allure.title("Отчёт по комнате содержит созданную бронь")
    def test_room_report_contains_booking(self, report_api, booked_period):
        response = report_api.get_room(ROOM_ID)
        assert response.status_code == 200

        periods = [(entry["start"], entry["end"])
                   for entry in response.json()["report"]]
        assert booked_period in periods

    @allure.title("Отчёт по всем комнатам доступен с токеном")
    def test_all_rooms_report_with_token(self, report_api, login):
        response = report_api.get_all()

        assert response.status_code == 200
        assert isinstance(response.json()["report"], list)

    @allure.title("Отчёт по всем комнатам требует токен")
    def test_all_rooms_report_requires_token(self, report_api):
        assert report_api.get_all().status_code == 400
