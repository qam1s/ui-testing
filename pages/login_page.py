import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

    def is_username_field_displayed(self) -> bool:
        return self.is_element_displayed(self.USERNAME_FIELD)

    @allure.step("Enter {username} in username field")
    def enter_username_field(self, username: str) -> None:
        self.fill_field(self.USERNAME_FIELD, username)

    def is_password_field_displayed(self) -> bool:
        return self.is_element_displayed(self.PASSWORD_FIELD)

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

    def get_username_description_field_title(self) -> str:
        return self.find_element(self.USERNAME_DESCRIPTION_FIELD_TITLE).text

    def is_login_button_disabled(self) -> bool:
        return (
            self.find_element(self.LOGIN_BUTTON).get_attribute("disabled")
            == "true"
        )

    @allure.step("Click Login button")
    def click_login_button(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.find_element(self.ERROR_MESSAGE).text

    def get_success_message(self) -> str:
        return self.find_element(self.SUCCESS_MESSAGE).text

    def is_error_message_displayed(self) -> bool:
        return self.is_element_displayed(self.ERROR_MESSAGE)

    def is_success_message_displayed(self) -> bool:
        return self.is_element_displayed(self.SUCCESS_MESSAGE)

    def wait_for_login_outcome(self, timeout: int = 10) -> str:
        def outcome(driver: WebDriver) -> str | bool:
            if driver.find_elements(*self.SUCCESS_MESSAGE):
                return "success"
            if driver.find_elements(*self.ERROR_MESSAGE):
                return "error"
            return False

        return WebDriverWait(self.driver, timeout).until(outcome)

    @allure.step("Click Logout button")
    def click_logout_button(self) -> None:
        for _ in range(3):
            self.click(self.LOGOUT_BUTTON)
            try:
                WebDriverWait(self.driver, 5).until(EC.url_contains("#/login"))
                return
            except TimeoutException:
                continue
        self.js_click(self.LOGOUT_BUTTON)
        WebDriverWait(self.driver, 5).until(EC.url_contains("#/login"))
