import random

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.bank_manager_login_page import BankManagerLoginPage


class OpenAccountPage(BankManagerLoginPage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://www.way2automation.com/angularjs-protractor/banking/#/manager/openAccount" # noqa
        self.CUSTOMER_DROPDOWN_LIST = (By.ID, "userSelect")
        self.CURRENCY_DROPDOWN_LIST = (By.ID, "currency")
        self.PROCESS_BUTTON = (By.XPATH, "//button[@type='submit']")

    @allure.step("Select customer")
    def select_customer(self, customer: str) -> None:
        self.select(
            self.CUSTOMER_DROPDOWN_LIST
        ).select_by_visible_text(customer)

    @allure.step("Select random currency")
    def select_random_currency(self) -> None:
        currency = random.choice(["Dollar", "Pound", "Rupee"])
        self.select(self.CURRENCY_DROPDOWN_LIST).select_by_value(currency)

    @allure.step("Click Process button")
    def click_process_button(self) -> None:
        self.click(self.PROCESS_BUTTON)
