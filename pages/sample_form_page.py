import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SampleFormPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://www.way2automation.com/angularjs-protractor/banking/registrationform.html" # noqa
        self.FIRST_NAME_FIELD = (By.ID, "firstName")
        self.LAST_NAME_FIELD = (By.ID, "lastName")
        self.EMAIL_FIELD = (By.ID, "email")
        self.PASSWORD_FIELD = (By.ID, "password")
        self.SPORTS_CHECKBOX = (By.XPATH, "//input[@value='Sports']")
        self.HOBBIES_CHECKBOXES = (By.XPATH, "//label/input")
        self.GENDER_DROPDOWN_LIST = (By.ID, "gender")
        self.ABOUT_YOURSELF_TEXTAREA = (By.ID, "about")
        self.REGISTER_BUTTON = (By.XPATH, "//div/button")
        self.SUCCESS_MESSAGE = (By.ID, "successMessage")

    @allure.step("Enter {first_name} in First Name field")
    def enter_first_name(self, first_name: str) -> None:
        self.fill_field(self.FIRST_NAME_FIELD, first_name)

    @allure.step("Enter {last_name} in Last Name field")
    def enter_last_name(self, last_name: str) -> None:
        self.fill_field(self.LAST_NAME_FIELD, last_name)

    @allure.step("Enter {email} in Email field")
    def enter_email(self, email: str) -> None:
        self.fill_field(self.EMAIL_FIELD, email)

    @allure.step("Enter {password} in Password field")
    def enter_password(self, password: str) -> None:
        self.fill_field(self.PASSWORD_FIELD, password)

    @allure.step("Select Sports checkbox in Hobbies block")
    def select_sports_hobby(self) -> None:
        self.click(self.SPORTS_CHECKBOX)

    def get_hobby_values(self) -> list[str]:
        return [
            str(hobby.get_attribute("value"))
            for hobby in self.find_elements(self.HOBBIES_CHECKBOXES)
        ]

    @allure.step("Select gender {gender} in Gender dropdown")
    def select_gender(self, gender: str) -> None:
        self.select(self.GENDER_DROPDOWN_LIST).select_by_value(gender)

    @allure.step("Enter {text} in About Yourself field")
    def enter_about_yourself(self, text: str) -> None:
        self.fill_field(self.ABOUT_YOURSELF_TEXTAREA, text)

    @allure.step("Click Register button")
    def click_register_button(self) -> None:
        self.click(self.REGISTER_BUTTON)

    def is_success_message_displayed(self) -> bool:
        return self.is_element_displayed(self.SUCCESS_MESSAGE)
