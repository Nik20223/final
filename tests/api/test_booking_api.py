"""API-тесты сервиса Booking."""

import allure
import pytest

pytestmark = pytest.mark.api

CHECKIN = "2030-01-10"
CHECKOUT = "2030-01-12"
NEW_CHECKIN = "2030-02-01"
NEW_CHECKOUT = "2030-02-03"


def booking_payload(checkin=CHECKIN, checkout=CHECKOUT):
    """Собрать тело брони с заданными датами."""
    return {
        "roomid": 1,
        "firstname": "Ivan",
        "lastname": "Petrov",
        "depositpaid": True,
        "bookingdates": {"checkin": checkin, "checkout": checkout},
    }


@pytest.fixture()
def login(auth_api):
    """Авторизует общую сессию под администратором."""
    return auth_api.login()


@pytest.fixture()
def created_booking(booking_api, login):
    """Создаёт бронь на время теста и удаляет её после."""
    response = booking_api.create(booking_payload())
    booking_id = response.json()["bookingid"]
    yield booking_id
    booking_api.delete(booking_id)


@allure.feature("Booking API")
class TestBookingApi:
    """CRUD и проверки доступа сервиса booking."""

    @allure.title("Создание брони возвращает 201")
    def test_create_booking(self, booking_api, login):
        response = booking_api.create(booking_payload())
        assert response.status_code == 201

        body = response.json()
        assert body["bookingid"] > 0
        assert body["booking"]["firstname"] == "Ivan"

        booking_api.delete(body["bookingid"])

    @allure.title("Бронь читается по id")
    def test_get_booking(self, booking_api, created_booking):
        response = booking_api.get(created_booking)
        assert response.status_code == 200
        assert response.json()["lastname"] == "Petrov"

    @allure.title("Обновление брони с новыми датами")
    def test_update_booking(self, booking_api, created_booking):
        payload = booking_payload(NEW_CHECKIN, NEW_CHECKOUT)
        response = booking_api.update(created_booking, payload)
        assert response.status_code == 200

    @allure.title("Удаление брони возвращает 202")
    def test_delete_booking(self, booking_api, created_booking):
        assert booking_api.delete(created_booking).status_code == 202
        assert booking_api.get(created_booking).status_code == 404

    @allure.title("Конфликт дат отклоняется с 409")
    def test_conflicting_dates_are_rejected(
        self, booking_api, login, created_booking
    ):
        response = booking_api.create(booking_payload())
        assert response.status_code == 409

    @allure.title("Список броней без токена запрещён")
    def test_get_all_requires_token(self, booking_api):
        assert booking_api.get_all().status_code == 403

    @allure.title("Список броней доступен с токеном")
    def test_get_all_with_token(self, booking_api, login, created_booking):
        response = booking_api.get_all(room_id=1)
        assert response.status_code == 200

    @allure.title("Занятые номера возвращаются списком")
    def test_unavailable_returns_rooms(self, booking_api):
        response = booking_api.unavailable(CHECKIN, CHECKOUT)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
