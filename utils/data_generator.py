"""Генерация уникальных тестовых данных."""

from datetime import date, timedelta
from uuid import uuid4

from faker import Faker

fake = Faker()

FIRSTNAME_MAX = 18
LASTNAME_MAX = 30
PHONE_LENGTH = 11


def unique_token():
    """Короткий уникальный суффикс, чтобы данные не пересекались."""
    return uuid4().hex[:8]


def room_name():
    """Уникальное имя комнаты."""
    return f"QA-Room-{unique_token()}"


def room_payload(name=None, room_type="Double", accessible=True, price=150):
    """Тело комнаты с корректными полями."""
    return {
        "roomName": name or room_name(),
        "type": room_type,
        "accessible": accessible,
        "roomPrice": price,
        "description": fake.sentence(nb_words=6),
        "features": ["WiFi", "TV"],
        "image": "https://example.com/room.jpg",
    }


def future_dates(start_in_days=45, nights=2):
    """Диапазон дат в будущем в формате YYYY-MM-DD."""
    checkin = date.today() + timedelta(days=start_in_days)
    checkout = checkin + timedelta(days=nights)
    return checkin.isoformat(), checkout.isoformat()


def contact():
    """Уникальные контакты, проходящие валидацию брони."""
    token = unique_token()
    return {
        "firstname": f"Qa{token[:6]}",
        "lastname": f"Test{token[:6]}",
        "email": f"qa.{token}@example.com",
        "phone": fake.numerify("#" * PHONE_LENGTH),
    }


def booking_payload(room_id, checkin, checkout):
    """Тело брони для заданной комнаты и дат."""
    payload = {
        "roomid": room_id,
        "depositpaid": True,
        "bookingdates": {"checkin": checkin, "checkout": checkout},
    }
    payload.update(contact())
    return payload
