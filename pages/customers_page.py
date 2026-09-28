import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.bank_manager_login_page import BankManagerLoginPage


class CustomersPage(BankManagerLoginPage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://www.way2automation.com/angularjs-protractor/banking/#/manager/list"  # noqa
        self.SEARCH_CUSTOMER_FIELD = (
            By.XPATH, "//input[@ng-model='searchCustomer']"
        )
        self.DELETE_CUSTOMER_BUTTON = (
            By.XPATH, "//button[@ng-click='deleteCust(cust)']"
        )
        self.CUSTOMERS_NAMES = (By.XPATH, "//tbody/tr/td[1]")

    @allure.step(
        "Enter customer name {customer_name} in Search Customer field"
    )
    def enter_customer_name(self, customer_name: str) -> None:
        self.fill_field(self.SEARCH_CUSTOMER_FIELD, customer_name)

    @allure.step("Clear Search Customer field")
    def clear_search_customer_field(self) -> None:
        self.clear_field(self.SEARCH_CUSTOMER_FIELD)

    def delete_customer_button_is_displayed(self) -> None:
        self.element_is_displayed(self.DELETE_CUSTOMER_BUTTON)

    @allure.step("Click Delete Customer button")
    def click_delete_customer_button(self) -> None:
        self.click(self.DELETE_CUSTOMER_BUTTON)

    def get_customers_names(self) -> list[str]:
        return [
            names.text for names in self.find_elements(self.CUSTOMERS_NAMES)
        ]
