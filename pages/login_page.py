import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://www.way2automation.com/angularjs-protractor/registeration/#/login"  # noqa
        self.USERNAME_FIELD = (By.ID, "username")
        self.PASSWORD_FIELD = (By.ID, "password")
        self.USERNAME_DESCRIPTION_FIELD = (
            By.XPATH, "//input[@id='formly_1_input_username_0']"
        )
        self.USERNAME_DESCRIPTION_FIELD_TITLE = (
            By.XPATH, "//label[@class='control-label ']"
        )
        self.LOGIN_BUTTON = (By.XPATH, "//button[@class='btn btn-danger']")
        self.ERROR_MESSAGE = (
            By.XPATH, "//div[@class='alert alert-danger ng-binding ng-scope']"
        )
        self.SUCCESS_MESSAGE = (
            By.XPATH, "(//p[@class='ng-scope'])[1]"
        )
        self.LOGOUT_BUTTON = (By.XPATH, "//p[@class='ng-scope']/a")

    def username_field_is_displayed(self) -> None:
        self.element_is_displayed(self.USERNAME_FIELD)

    @allure.step("Enter {username} in username field")
    def enter_username_field(self, username: str) -> None:
        self.fill_field(self.USERNAME_FIELD, username)

    def password_field_is_displayed(self) -> None:
        self.element_is_displayed(self.PASSWORD_FIELD)

    @allure.step("Enter {password} in password field")
    def enter_password_field(self, password: str) -> None:
        self.fill_field(self.PASSWORD_FIELD, password)

    @allure.step("Enter {username_description} in username description field")
    def enter_username_description_field(
        self, username_description: str
    ) -> None:
        self.fill_field(
            self.USERNAME_DESCRIPTION_FIELD, username_description
        )

    def find_username_description_field_title(self) -> WebElement:
        return self.find_element(self.USERNAME_DESCRIPTION_FIELD_TITLE)

    def find_login_button(self) -> WebElement:
        return self.find_element(self.LOGIN_BUTTON)

    @allure.step("Click Login button")
    def click_login_button(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def find_error_message(self) -> WebElement:
        return self.find_element(self.ERROR_MESSAGE)

    def find_success_message(self) -> WebElement:
        return self.find_element(self.SUCCESS_MESSAGE)

    @allure.step("Click Logout button")
    def click_logout_button(self) -> None:
        self.click(self.LOGOUT_BUTTON)
