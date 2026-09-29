"""Базовый класс Page Object с общими действиями для страниц."""

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:
    """Общие методы взаимодействия со страницей через Selenium WebDriver."""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        """Принять WebDriver и таймаут ожиданий по умолчанию."""
        self.driver = driver
        self.timeout = timeout

    def open(self, url):
        """Открыть переданный URL в браузере."""
        self.driver.get(url)

    def find_element(self, locator):
        """Найти элемент по локатору вида ``(By.<STRATEGY>, "value")``."""
        return self.driver.find_element(*locator)

    def wait_for_element(self, locator, timeout=DEFAULT_TIMEOUT):
        """Дождаться появления элемента в DOM и вернуть его."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        """Дождаться кликабельности, прокрутить к элементу и кликнуть."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center',"
            " behavior: 'instant'});",
            element,
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        """Очистить поле и ввести в него текст."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Вернуть текст элемента, дождавшись его видимости."""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def is_element_visible(self, locator):
        """Вернуть ``True``, если элемент виден, иначе ``False``."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
