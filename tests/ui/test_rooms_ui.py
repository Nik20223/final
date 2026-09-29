"""UI-тесты управления комнатами в админ-панели."""

import allure
import pytest

from pages.room_page import RoomPage
from utils.data_generator import room_name

pytestmark = pytest.mark.ui


@pytest.fixture()
def admin_rooms(admin):
    """Открывает под администратором страницу комнат."""
    return RoomPage(admin).open()


@allure.feature("Комнаты (UI)")
class TestRoomsUi:
    """Создание, отображение и удаление комнат через админку."""

    @allure.title("Комната создаётся и удаляется")
    def test_create_and_delete_room(self, admin_rooms):
        name = room_name()

        admin_rooms.create_room(name, "Double", "true", "150")
        admin_rooms.wait_for_room(name)
        assert admin_rooms.has_room(name)

        admin_rooms.delete_room(name)
        admin_rooms.wait_for_room_removed(name)
        assert not admin_rooms.has_room(name)

    @allure.title("Созданная комната показывает тип и цену")
    def test_created_room_shows_type_and_price(self, admin_rooms):
        name = room_name()

        admin_rooms.create_room(name, "Suite", "true", "321")
        admin_rooms.wait_for_room(name)

        assert admin_rooms.room_type(name) == "Suite"
        assert admin_rooms.room_price(name) == "321"

        admin_rooms.delete_room(name)
        admin_rooms.wait_for_room_removed(name)

    @allure.title("Комната сохраняется после перезагрузки страницы")
    def test_created_room_persists_after_reload(self, admin_rooms):
        name = room_name()

        admin_rooms.create_room(name, "Twin", "false", "99")
        admin_rooms.wait_for_room(name)

        admin_rooms.open()
        admin_rooms.wait_for_room(name)
        assert admin_rooms.has_room(name)

        admin_rooms.delete_room(name)
        admin_rooms.wait_for_room_removed(name)
