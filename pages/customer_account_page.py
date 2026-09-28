import time

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CustomerAccountPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = (
            "https://www.way2automation.com/angularjs-protractor/banking/#/account"
        )
        self.CUSTOMER_WELCOME_MESSAGE = (By.XPATH, "//strong/span")
        self.CUSTOMER_BALANCE = (By.XPATH, "//div/strong[@class='ng-binding'][2]")
        self.TRANSACTIONS_BUTTON = (By.XPATH, "//button[@ng-click='transactions()']")
        self.DEPOSIT_BUTTON = (By.XPATH, "//button[@ng-click='deposit()']")
        self.WITHDRAW_BUTTON = (By.XPATH, "//button[@ng-click='withdrawl()']")
        self.AMOUNT_FIELD = (By.XPATH, "//input[@ng-model='amount']")
        self.INFO_MESSAGE = (By.XPATH, "//span[@ng-show='message']")
        self.SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
        self.DATE_TIME_SORT_BUTTON = (By.XPATH, "//a[@href='#']")
        self.TABLE_TRANSACTIONS = (By.XPATH, "//tbody/tr")
        self.LAST_TRANSACTION_AMOUNT = (By.XPATH, "//tr[@id='anchor0']/td[2]")
        self.LAST_TRANSACTION_TYPE = (By.XPATH, "//tr[@id='anchor0']/td[3]")
        self.RESET_BUTTON = (By.XPATH, "//button[@ng-click='reset()']")
        self.BACK_BUTTON = (By.XPATH, "//button[@ng-click='back()']")

    def get_customer_welcome_message(self) -> str:
        return self.find_element(self.CUSTOMER_WELCOME_MESSAGE).text

    def get_customer_balance(self) -> str:
        return self.find_element(self.CUSTOMER_BALANCE).text

    def get_transactions_count(self) -> int:
        return len(self.driver.find_elements(*self.TABLE_TRANSACTIONS))

    def get_transaction_rows_text(self) -> list[str]:
        return [
            row.text for row in self.driver.find_elements(*self.TABLE_TRANSACTIONS)
        ]

    @allure.step("Click Transactions button")
    def click_transactions_button(self) -> None:
        self.click(self.TRANSACTIONS_BUTTON)

    def open_transactions_and_wait(self, timeout: int = 20) -> None:
        deadline = time.monotonic() + timeout
        while True:
            self.click(self.TRANSACTIONS_BUTTON)
            try:
                self.wait_for_transactions_view(timeout=5)
            except TimeoutException:
                if time.monotonic() >= deadline:
                    raise
                continue
            try:
                self.wait_for_transactions(timeout=5)
                return
            except TimeoutException:
                if time.monotonic() >= deadline:
                    raise
                self.click(self.BACK_BUTTON)

    def wait_for_transactions_view(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.BACK_BUTTON)
        )

    def get_submit_button_text(self) -> str:
        return self.find_element(self.SUBMIT_BUTTON).text

    def wait_for_form(self, name: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: any(
                name in button.text
                for button in driver.find_elements(*self.SUBMIT_BUTTON)
            )
        )

    def _click_tab_until_form(
        self, locator: tuple, form_name: str, attempts: int = 3
    ) -> None:
        for attempt in range(attempts):
            self.click(locator)
            try:
                self.wait_for_form(form_name, timeout=5)
                return
            except TimeoutException:
                if attempt == attempts - 1:
                    raise

    def wait_for_transactions(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.TABLE_TRANSACTIONS)
        )

    def wait_until_transactions_empty(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: len(driver.find_elements(*self.TABLE_TRANSACTIONS)) == 0
        )

    @allure.step("Click Deposit button")
    def click_deposit_button(self) -> None:
        self._click_tab_until_form(self.DEPOSIT_BUTTON, "Deposit")

    @allure.step("Click Withdraw button")
    def click_withdraw_button(self) -> None:
        self._click_tab_until_form(self.WITHDRAW_BUTTON, "Withdraw")

    @allure.step("Enter amount {amount} in Amount field")
    def enter_amount(self, amount: str) -> None:
        self.clear_field(self.AMOUNT_FIELD)
        self.fill_field(self.AMOUNT_FIELD, amount)

    @allure.step("Click Submit button")
    def click_submit_button(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Click Reset button")
    def click_reset_button(self) -> None:
        self.click(self.RESET_BUTTON)

    @allure.step("Click Back button")
    def click_back_button(self) -> None:
        self.click(self.BACK_BUTTON)

    def is_info_message_displayed(self) -> bool:
        return self.find_element(self.INFO_MESSAGE).is_displayed()

    def get_info_message(self) -> str:
        return self.find_element(self.INFO_MESSAGE).text

    def wait_for_info_message(self, text: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: any(
                text in message.text
                for message in driver.find_elements(*self.INFO_MESSAGE)
            )
        )

    def sort_transactions_by_date(self) -> None:
        self.click(self.DATE_TIME_SORT_BUTTON)

    def get_last_transaction(self) -> tuple[str, str]:
        transaction_type = self.find_element(self.LAST_TRANSACTION_TYPE).text
        amount = self.find_element(self.LAST_TRANSACTION_AMOUNT).text
        return transaction_type, amount
