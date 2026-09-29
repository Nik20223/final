"""Конфигурация тестового проекта Restful Booker Platform.

Значения можно переопределять переменными окружения — это удобно, чтобы
гонять тесты и на локальном стенде (docker compose), и на публичном.
"""

import os

# --- Адреса -------------------------------------------------------------
# Стенд развёрнут на сервере: UI на 80, API-сервисы на портах 3000-3006.
# Для локального стенда задайте RBP_API_HOST и RBP_UI_URL = http://localhost.
API_HOST = os.getenv("RBP_API_HOST", "http://147.78.67.204")
UI_BASE_URL = os.getenv("RBP_UI_URL", "http://147.78.67.204")
ADMIN_URL = os.getenv("RBP_ADMIN_URL", f"{UI_BASE_URL}/admin")

BOOKING_API_URL = os.getenv("RBP_BOOKING_URL", f"{API_HOST}:3000/booking")
ROOM_API_URL = os.getenv("RBP_ROOM_URL", f"{API_HOST}:3001/room")
BRANDING_API_URL = os.getenv("RBP_BRANDING_URL", f"{API_HOST}:3002/branding")
AUTH_API_URL = os.getenv("RBP_AUTH_URL", f"{API_HOST}:3004/auth")
REPORT_API_URL = os.getenv("RBP_REPORT_URL", f"{API_HOST}:3005/report")
MESSAGE_API_URL = os.getenv("RBP_MESSAGE_URL", f"{API_HOST}:3006/message")

# --- Учётные данные администратора --------------------------------------
ADMIN_USERNAME = os.getenv("RBP_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("RBP_ADMIN_PASSWORD", "password")

# --- Таймауты (в секундах) ----------------------------------------------
DEFAULT_TIMEOUT = int(os.getenv("RBP_DEFAULT_TIMEOUT", "10"))
PAGE_LOAD_TIMEOUT = int(os.getenv("RBP_PAGE_LOAD_TIMEOUT", "30"))

# --- Браузер ------------------------------------------------------------
BROWSER = os.getenv("RBP_BROWSER", "chrome")
HEADLESS = os.getenv("RBP_HEADLESS", "false").strip().lower() in {"1", "true", "yes"}
