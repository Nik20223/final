"""API-тесты сервиса комнат."""

import allure
import pytest

from utils.data_generator import room_payload

pytestmark = pytest.mark.api


@pytest.fixture()
def login(auth_api):
    """Авторизует общую сессию под администратором."""
    return auth_api.login()


@pytest.fixture()
def created_room(room_api, login):
    """Создаёт комнату на время теста и удаляет её после."""
    response = room_api.create(room_payload())
    room_id = response.json()["roomid"]
    yield room_id
    room_api.delete(room_id)


@allure.feature("Room API")
class TestRoomApi:
    """CRUD и проверки доступа сервиса комнат."""

    @allure.title("Список комнат доступен без токена")
    def test_get_all_rooms(self, room_api):
        response = room_api.get_all()

        assert response.status_code == 200
        assert response.json()["rooms"]

    @allure.title("Комната читается по id")
    def test_get_room(self, room_api, created_room):
        response = room_api.get(created_room)

        assert response.status_code == 200
        assert response.json()["roomid"] == created_room

    @allure.title("Создание комнаты возвращает 201")
    def test_create_room(self, room_api, login):
        payload = room_payload()

        response = room_api.create(payload)

        assert response.status_code == 201
        assert response.json()["roomName"] == payload["roomName"]
        room_api.delete(response.json()["roomid"])

    @allure.title("Обновление комнаты меняет цену")
    def test_update_room(self, room_api, created_room):
        response = room_api.update(created_room, room_payload(price=250))

        assert response.status_code == 202
        assert response.json()["roomPrice"] == 250

    @allure.title("Удалённая комната исчезает из списка")
    def test_delete_room(self, room_api, created_room):
        assert room_api.delete(created_room).status_code == 202

        room_ids = [room["roomid"]
                    for room in room_api.get_all().json()["rooms"]]
        assert created_room not in room_ids

    @allure.title("Создание комнаты без токена запрещено")
    def test_create_requires_token(self, room_api):
        assert room_api.create(room_payload()).status_code == 403

    @allure.title("Недопустимый тип комнаты отклоняется")
    def test_create_with_invalid_type(self, room_api, login):
        payload = room_payload()
        payload["type"] = "Penthouse"

        assert room_api.create(payload).status_code == 400
