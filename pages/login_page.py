"""Page Object страницы входа в админ-панель."""

from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Форма входа на /admin."""

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "doLogin")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")

    def open(self):
        """Открыть страницу входа."""
        super().open(config.ADMIN_URL)
        return self

    def login(self, username, password):
        """Заполнить форму входа и отправить её."""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def is_error_displayed(self):
        """Показано ли сообщение об ошибке авторизации."""
        return self.is_element_visible(self.ERROR_ALERT)

    def error_message(self):
        """Текст сообщения об ошибке авторизации."""
        return self.get_text(self.ERROR_ALERT)
