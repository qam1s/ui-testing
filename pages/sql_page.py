import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


class SQLPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://www.sql-ex.ru/"
        self.LOGIN = "losoxo@azuretechtalk."
        self.LOGIN_FIELD = (By.XPATH, "(//input[@type='text'])[1]")
        self.PASSWORD = "losoxo@azuretechtalk.net"
        self.PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
        self.NICKNAME = "losoxo@azuretechtalk"
        self.ENTER_BUTTON = (By.XPATH, "(//input[@type='submit'])[1]")
        self.RIGHT_HEADER = (By.XPATH, "(//td[@align='right'])[1]")

    def find_login_field(self) -> WebElement:
        return self.find_element(self.LOGIN_FIELD)

    @allure.step("Enter {login} in Login field")
    def enter_login(self, login: str) -> None:
        self.fill_field(self.LOGIN_FIELD, login)

    @allure.step("Enter {password} in Password field")
    def enter_password(self, password: str) -> None:
        self.fill_field(self.PASSWORD_FIELD, password)

    @allure.step("Click Enter button")
    def click_enter_button(self) -> None:
        self.click(self.ENTER_BUTTON)

    def find_right_header(self) -> WebElement:
        return self.find_element(self.RIGHT_HEADER)
