"""Хелперы для сервиса Booking Restful Booker Platform."""

from api.api_client import ApiClient
from config import config


class BookingApi:
    """CRUD-операции сервиса booking и вспомогательные выборки."""

    def __init__(self, base_url=None, session=None, timeout=None):
        """Клиент сервиса booking; сессию можно разделить с auth."""
        self.client = ApiClient(
            base_url or config.BOOKING_API_URL,
            session=session,
            timeout=timeout,
        )

    def create(self, booking):
        """Создать бронь (POST /)."""
        return self.client.post("/", json=booking)

    def get(self, booking_id):
        """Получить бронь по id (GET /{id})."""
        return self.client.get(f"/{booking_id}")

    def get_all(self, room_id=None):
        """Получить список броней (GET /), опционально по комнате."""
        params = {"roomid": room_id} if room_id is not None else None
        return self.client.get("/", params=params)

    def update(self, booking_id, booking):
        """Обновить бронь (PUT /{id})."""
        return self.client.put(f"/{booking_id}", json=booking)

    def delete(self, booking_id):
        """Удалить бронь (DELETE /{id})."""
        return self.client.delete(f"/{booking_id}")

    def unavailable(self, checkin, checkout):
        """Вернуть занятые номера за период (GET /unavailable)."""
        params = {"checkin": checkin, "checkout": checkout}
        return self.client.get("/unavailable", params=params)

    def summary(self, room_id):
        """Сводка по комнате (GET /summary)."""
        return self.client.get("/summary", params={"roomid": room_id})
