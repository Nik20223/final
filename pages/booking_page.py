"""Page Object публичной формы бронирования."""

from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class BookingPage(BasePage):
    """Страница бронирования комнаты посетителем (/reservation/{id})."""

    RESERVE_BUTTON = (By.ID, "doReservation")
    FIRSTNAME_INPUT = (By.CSS_SELECTOR, "input.room-firstname")
    LASTNAME_INPUT = (By.CSS_SELECTOR, "input.room-lastname")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input.room-email")
    PHONE_INPUT = (By.CSS_SELECTOR, "input.room-phone")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Reserve Now']")
    CONFIRMATION = (By.XPATH, "//h2[text()='Booking Confirmed']")

    def open(self, room_id, checkin, checkout):
        """Открыть страницу комнаты с выбранными датами."""
        url = (
            f"{config.UI_BASE_URL}/reservation/{room_id}"
            f"?checkin={checkin}&checkout={checkout}"
        )
        super().open(url)
        return self

    def start_booking(self):
        """Нажать «Reserve Now» на календаре, чтобы открыть форму."""
        self.click(self.RESERVE_BUTTON)
        return self

    def fill_details(self, firstname, lastname, email, phone):
        """Заполнить контактные поля брони."""
        self.type_text(self.FIRSTNAME_INPUT, firstname)
        self.type_text(self.LASTNAME_INPUT, lastname)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PHONE_INPUT, phone)
        return self

    def submit(self):
        """Отправить форму бронирования."""
        self.click(self.SUBMIT_BUTTON)
        return self

    def is_confirmed(self):
        """Показан ли экран подтверждения брони."""
        return self.is_element_visible(self.CONFIRMATION)
