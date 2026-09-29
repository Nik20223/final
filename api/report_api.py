"""Хелперы для сервиса отчётов Restful Booker Platform."""

from api.api_client import ApiClient
from config import config


class ReportApi:
    """Отчёты по занятости комнат."""

    def __init__(self, base_url=None, session=None, timeout=None):
        """Клиент сервиса отчётов; сессию можно разделить с auth."""
        self.client = ApiClient(
            base_url or config.REPORT_API_URL,
            session=session,
            timeout=timeout,
        )

    def get_all(self):
        """Отчёт по всем комнатам (GET /), требует токен."""
        return self.client.get("/")

    def get_room(self, room_id):
        """Отчёт по конкретной комнате (GET /room/{id})."""
        return self.client.get(f"/room/{room_id}")
