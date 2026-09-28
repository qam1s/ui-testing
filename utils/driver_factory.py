import os
from typing import Union, cast

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

WebDriverOptions = Union[ChromeOptions, FirefoxOptions, EdgeOptions]


class DriverFactory:
    GRID_URL = os.getenv("GRID_URL", "http://localhost:4444")

    @staticmethod
    def get_driver(grid: bool, browser: str) -> WebDriver:
        options = DriverFactory._options(browser)
        DriverFactory._arguments(options)
        if grid:
            return webdriver.Remote(
                command_executor=DriverFactory.GRID_URL, options=options
            )
        return DriverFactory._driver(browser, options)

    @staticmethod
    def _options(browser: str) -> WebDriverOptions:
        match browser:
            case "chrome":
                return ChromeOptions()
            case "firefox":
                return FirefoxOptions()
            case "edge":
                return EdgeOptions()
            case _:
                raise ValueError(f"Invalid browser name: {browser}")

    @staticmethod
    def _arguments(options: WebDriverOptions) -> None:
        if os.getenv("HEADLESS", "true").lower() not in ("0", "false", "no"):
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    @staticmethod
    def _driver(browser: str, options: WebDriverOptions) -> WebDriver:
        match browser:
            case "chrome":
                return webdriver.Chrome(cast(ChromeOptions, options))
            case "firefox":
                return webdriver.Firefox(cast(FirefoxOptions, options))
            case "edge":
                return webdriver.Edge(cast(EdgeOptions, options))
            case _:
                raise ValueError(f"Invalid browser name: {browser}")
