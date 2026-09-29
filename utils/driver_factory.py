"""Фабрика WebDriver для UI-тестов."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import config

_BROWSER_BUILDERS = {
    "chrome": "_build_chrome",
    "firefox": "_build_firefox",
}


class DriverFactory:
    """Создаёт настроенный экземпляр WebDriver под нужный браузер."""

    @staticmethod
    def create(browser=None, headless=None):
        """Собрать WebDriver: браузер и режим берутся из конфига."""
        name = (browser or config.BROWSER).strip().lower()
        if name not in _BROWSER_BUILDERS:
            raise ValueError(f"Неподдерживаемый браузер: {name}")
        if headless is None:
            headless = config.HEADLESS

        builder = getattr(DriverFactory, _BROWSER_BUILDERS[name])
        driver = builder(headless)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        return driver

    @staticmethod
    def _build_chrome(headless):
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)

    @staticmethod
    def _build_firefox(headless):
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if headless:
            options.add_argument("-headless")
        return webdriver.Firefox(options=options)
