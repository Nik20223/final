"""Обёртка над requests.Session для вызовов API платформы."""

import requests

from config import config


class ApiClient:
    """HTTP-клиент с базовым URL, таймаутом и общей сессией."""

    def __init__(self, base_url, session=None, timeout=None):
        """Задать базовый URL; сессию и таймаут можно передать снаружи."""
        self.base_url = base_url.rstrip("/")
        self.timeout = config.DEFAULT_TIMEOUT if timeout is None else timeout
        self.session = session if session is not None else requests.Session()
        self.session.headers.setdefault("Accept", "application/json")

    def _build_url(self, path):
        """Склеить базовый URL с путём, убрав лишние слэши."""
        return f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url

    def request(self, method, path="", **kwargs):
        """Выполнить запрос, подставив таймаут по умолчанию."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, self._build_url(path), **kwargs)

    def get(self, path="", **kwargs):
        """Отправить GET-запрос."""
        return self.request("GET", path, **kwargs)

    def post(self, path="", **kwargs):
        """Отправить POST-запрос."""
        return self.request("POST", path, **kwargs)

    def put(self, path="", **kwargs):
        """Отправить PUT-запрос."""
        return self.request("PUT", path, **kwargs)

    def patch(self, path="", **kwargs):
        """Отправить PATCH-запрос."""
        return self.request("PATCH", path, **kwargs)

    def delete(self, path="", **kwargs):
        """Отправить DELETE-запрос."""
        return self.request("DELETE", path, **kwargs)

    def close(self):
        """Закрыть сессию и освободить соединения."""
        self.session.close()
