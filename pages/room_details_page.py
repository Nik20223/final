"""Page Object страницы комнаты в админ-панели."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import config
from pages.base_page import BasePage


class RoomDetailsPage(BasePage):
    """Просмотр и правка комнаты на /admin/room/{id}."""

    TITLE = (By.CSS_SELECTOR, ".room-details h2")
    TYPE_VALUE = (
        By.XPATH,
        "//div[contains(@class,'room-details')]"
        "//p[starts-with(normalize-space(),'Type:')]/span",
    )
    PRICE_VALUE = (
        By.XPATH,
        "//div[contains(@class,'room-details')]"
        "//p[starts-with(normalize-space(),'Room price:')]/span",
    )
    EDIT_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'room-details')]"
        "//button[normalize-space()='Edit']",
    )
    PRICE_INPUT = (By.ID, "roomPrice")
    UPDATE_BUTTON = (By.ID, "update")
    BOOKING_ROWS = (By.CSS_SELECTOR, "div.detail")

    def open(self, room_id):
        """Открыть страницу комнаты в админке."""
        super().open(f"{config.UI_BASE_URL}/admin/room/{room_id}")
        return self

    def room_name(self):
        """Имя комнаты без префикса «Room:»."""
        return self.get_text(self.TITLE).replace("Room:", "").strip()

    def room_type(self):
        """Тип комнаты."""
        return self.get_text(self.TYPE_VALUE)

    def room_price(self):
        """Цена комнаты."""
        return self.get_text(self.PRICE_VALUE)

    def booking_lastnames(self):
        """Фамилии всех броней комнаты."""
        lastnames = []
        for row in self.driver.find_elements(*self.BOOKING_ROWS):
            cells = row.find_elements(By.CSS_SELECTOR, "div.col-sm-2 p")
            if len(cells) >= 2:
                lastnames.append(cells[1].text)
        return lastnames

    def has_booking(self, lastname):
        """Есть ли среди броней комнаты запись с такой фамилией."""
        return lastname in self.booking_lastnames()

    def wait_for_booking(self, lastname, timeout=None):
        """Дождаться появления брони с заданной фамилией."""
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda _: lastname in self.booking_lastnames()
        )
        return self

    def start_edit(self):
        """Перейти в режим редактирования комнаты."""
        self.click(self.EDIT_BUTTON)
        return self

    def set_price(self, price):
        """Задать новую цену комнаты."""
        self.type_text(self.PRICE_INPUT, str(price))
        return self

    def save(self):
        """Сохранить изменения комнаты."""
        self.click(self.UPDATE_BUTTON)
        return self
