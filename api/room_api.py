"""Хелперы для сервиса комнат Restful Booker Platform."""

from api.api_client import ApiClient
from config import config


class RoomApi:
    """CRUD-операции сервиса room."""

    def __init__(self, base_url=None, session=None, timeout=None):
        """Клиент сервиса комнат; сессию можно разделить с auth."""
        self.client = ApiClient(
            base_url or config.ROOM_API_URL,
            session=session,
            timeout=timeout,
        )

    def get_all(self, checkin=None, checkout=None):
        """Список комнат (GET /) либо занятые номера за период."""
        params = None
        if checkin and checkout:
            params = {"checkin": checkin, "checkout": checkout}
        return self.client.get("/", params=params)

    def get(self, room_id):
        """Получить комнату по id (GET /{id})."""
        return self.client.get(f"/{room_id}")

    def create(self, room):
        """Создать комнату (POST /)."""
        return self.client.post("/", json=room)

    def update(self, room_id, room):
        """Обновить комнату (PUT /{id})."""
        return self.client.put(f"/{room_id}", json=room)

    def delete(self, room_id):
        """Удалить комнату (DELETE /{id})."""
        return self.client.delete(f"/{room_id}")
