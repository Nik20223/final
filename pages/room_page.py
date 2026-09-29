"""Page Object админ-страницы управления комнатами."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from config import config
from pages.base_page import BasePage


class RoomPage(BasePage):
    """Список комнат и форма создания на /admin/rooms."""

    ROOM_ROWS = (By.CSS_SELECTOR, "[data-testid='roomlisting']")
    ROOM_NAME_CELLS = (By.CSS_SELECTOR, "p[id^='roomName']")
    NAME_INPUT = (By.CSS_SELECTOR, "[data-testid='roomName']")
    TYPE_SELECT = (By.ID, "type")
    ACCESSIBLE_SELECT = (By.ID, "accessible")
    PRICE_INPUT = (By.ID, "roomPrice")
    CREATE_BUTTON = (By.ID, "createRoom")
    LOGOUT_BUTTON = (By.XPATH, "//button[normalize-space()='Logout']")

    def open(self):
        """Открыть страницу со списком комнат."""
        super().open(f"{config.UI_BASE_URL}/admin/rooms")
        return self

    def create_room(self, name, room_type="Single",
                    accessible="false", price="100"):
        """Заполнить форму создания комнаты и отправить её."""
        self.type_text(self.NAME_INPUT, name)
        self._select(self.TYPE_SELECT, room_type)
        self._select(self.ACCESSIBLE_SELECT, accessible)
        self.type_text(self.PRICE_INPUT, str(price))
        self.click(self.CREATE_BUTTON)
        return self

    def room_names(self):
        """Имена всех комнат в списке."""
        cells = self.driver.find_elements(*self.ROOM_NAME_CELLS)
        return [cell.text for cell in cells]

    def has_room(self, name):
        """Есть ли в списке комната с таким именем."""
        return name in self.room_names()

    def room_row(self, name):
        """Строка комнаты с заданным именем."""
        return self.wait_for_element((
            By.XPATH,
            "//div[@data-testid='roomlisting']"
            f"[.//p[starts-with(@id,'roomName')]"
            f"[normalize-space()='{name}']]",
        ))

    def room_type(self, name):
        """Тип комнаты из её строки в списке."""
        row = self.room_row(name)
        return row.find_element(
            By.XPATH, ".//p[starts-with(@id,'type')]"
        ).text

    def room_price(self, name):
        """Цена комнаты из её строки в списке."""
        row = self.room_row(name)
        return row.find_element(
            By.XPATH, ".//p[starts-with(@id,'roomPrice')]"
        ).text

    def logout(self):
        """Выйти из админ-панели."""
        self.click(self.LOGOUT_BUTTON)
        return self

    def wait_for_room(self, name, timeout=None):
        """Дождаться появления комнаты в списке."""
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(self._name_locator(name))
        )
        return self

    def wait_for_room_removed(self, name, timeout=None):
        """Дождаться исчезновения комнаты из списка."""
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.invisibility_of_element_located(self._name_locator(name))
        )
        return self

    def delete_room(self, name):
        """Удалить комнату с заданным именем."""
        locator = (
            By.XPATH,
            "//div[@data-testid='roomlisting']"
            f"[.//p[starts-with(@id,'roomName')][normalize-space()='{name}']]"
            "//span[contains(@class,'roomDelete')]",
        )
        self.click(locator)
        return self

    @staticmethod
    def _name_locator(name):
        """Локатор ячейки с именем комнаты."""
        return (
            By.XPATH,
            "//p[starts-with(@id,'roomName')]"
            f"[normalize-space()='{name}']",
        )

    def _select(self, locator, value):
        """Выбрать опцию выпадающего списка по видимому тексту."""
        element = self.wait_for_element(locator)
        Select(element).select_by_visible_text(value)
