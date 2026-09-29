"""UI-тесты бронирования комнаты посетителем."""

import allure
import pytest

from pages.booking_page import BookingPage
from pages.room_details_page import RoomDetailsPage
from utils.data_generator import contact, future_dates

pytestmark = pytest.mark.ui

ROOM_ID = 1


@pytest.fixture()
def booking(booking_api, auth_api):
    """Уникальные данные брони; после теста бронь удаляется через API."""
    checkin, checkout = future_dates(start_in_days=60, nights=2)
    data = {"checkin": checkin, "checkout": checkout, **contact()}

    yield data

    auth_api.login()
    response = booking_api.get_all(ROOM_ID)
    if response.status_code != 200:
        return
    for item in response.json().get("bookings", []):
        if item.get("firstname") == data["firstname"]:
            booking_api.delete(item["bookingid"])


def reserve_room(driver, data):
    """Бронирует комнату через публичную форму."""
    page = BookingPage(driver).open(
        ROOM_ID, data["checkin"], data["checkout"]
    )
    page.start_booking()
    page.fill_details(
        data["firstname"], data["lastname"], data["email"], data["phone"]
    )
    page.submit()
    return page


@allure.feature("Бронирование (UI)")
class TestBookingUi:
    """Бронирование комнаты из публичной части."""

    @allure.title("Комната бронируется с публичной страницы")
    def test_reserve_room(self, driver, booking):
        assert reserve_room(driver, booking).is_confirmed()

    @allure.title("Созданная бронь видна в админке на странице комнаты")
    def test_booking_appears_in_admin_room_page(self, driver, booking, admin):
        assert reserve_room(driver, booking).is_confirmed()

        page = RoomDetailsPage(driver).open(ROOM_ID)
        page.wait_for_booking(booking["lastname"])
        assert page.has_booking(booking["lastname"])
