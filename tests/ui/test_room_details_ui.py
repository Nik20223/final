"""UI-тесты страницы комнаты в админ-панели."""

import allure
import pytest

from pages.room_details_page import RoomDetailsPage
from utils.data_generator import room_payload

pytestmark = pytest.mark.ui


@pytest.fixture()
def room(room_api, auth_api):
    """Создаёт комнату через API и удаляет её после теста."""
    auth_api.login()
    created = room_api.create(room_payload()).json()

    yield created
    room_api.delete(created["roomid"])


@allure.feature("Страница комнаты (UI)")
class TestRoomDetailsUi:
    """Просмотр и правка комнаты из админки."""

    @allure.title("Страница комнаты показывает её данные")
    def test_room_details_show_room_info(self, admin, room):
        page = RoomDetailsPage(admin).open(room["roomid"])

        assert page.room_name() == room["roomName"]
        assert page.room_type() == room["type"]
        assert page.room_price() == str(room["roomPrice"])

    @allure.title("Цену комнаты можно изменить из админки")
    def test_update_room_price_from_admin(self, admin, room):
        page = RoomDetailsPage(admin).open(room["roomid"])
        page.start_edit().set_price(777).save()

        updated = RoomDetailsPage(admin).open(room["roomid"])
        assert updated.room_price() == "777"
