import allure
import pytest
from faker import Faker
from selenium.webdriver.remote.webdriver import WebDriver

from data.test_data import Customer
from pages.add_customer_page import AddCustomerPage
from pages.bank_manager_login_page import BankManagerLoginPage
from pages.banking_app_page import BankingAppPage
from pages.customer_account_page import CustomerAccountPage
from pages.customer_login_page import CustomerLoginPage
from pages.customers_page import CustomersPage
from pages.open_account_page import OpenAccountPage
from pages.sample_form_page import SampleFormPage


def _customer_full_name(customer: Customer) -> str:
    return f"{customer.first_name} {customer.last_name}"


def _add_customer(driver: WebDriver, customer: Customer) -> str:
    banking_app_page = BankingAppPage(driver)
    banking_app_page.open_page()
    banking_app_page.click_bank_manager_login_button()
    bank_manager_login_page = BankManagerLoginPage(driver)
    bank_manager_login_page.page_is_opened()
    bank_manager_login_page.click_add_customer_button()
    add_customer_page = AddCustomerPage(driver)
    add_customer_page.page_is_opened()
    add_customer_page.enter_first_name(customer.first_name)
    add_customer_page.enter_last_name(customer.last_name)
    add_customer_page.enter_post_code(customer.post_code)
    add_customer_page.click_add_customer_button_2()
    alert = add_customer_page.get_alert()
    text = alert.text
    alert.accept()
    return text


def _open_account(driver: WebDriver, customer_name: str) -> str:
    open_account_page = OpenAccountPage(driver)
    open_account_page.open_page()
    open_account_page.select_customer(customer_name)
    open_account_page.select_currency("Dollar")
    open_account_page.click_process_button()
    alert = open_account_page.get_alert()
    text = alert.text
    alert.accept()
    return text


def _login_as_customer(
    driver: WebDriver, customer_name: str
) -> CustomerAccountPage:
    banking_app_page = BankingAppPage(driver)
    banking_app_page.open_page()
    banking_app_page.click_customer_login_button()
    customer_login_page = CustomerLoginPage(driver)
    customer_login_page.select_customer(customer_name)
    customer_login_page.click_login_button()
    return CustomerAccountPage(driver)


def _table_balance(rows: list[str]) -> int:
    total = 0
    for row in rows:
        parts = row.split()
        amount, transaction_type = int(parts[-2]), parts[-1]
        total += amount if transaction_type == "Credit" else -amount
    return total


@pytest.fixture
def logged_in_account(driver: WebDriver, customer: Customer) -> CustomerAccountPage:
    _add_customer(driver, customer)
    _open_account(driver, _customer_full_name(customer))
    return _login_as_customer(driver, _customer_full_name(customer))


@pytest.fixture
def funded_account(
    logged_in_account: CustomerAccountPage,
) -> CustomerAccountPage:
    logged_in_account.click_deposit_button()
    logged_in_account.enter_amount("100")
    logged_in_account.click_submit_button()
    logged_in_account.wait_for_info_message("Deposit Successful")
    assert logged_in_account.get_info_message() == "Deposit Successful"
    return logged_in_account


@allure.epic("UI")
@allure.feature("Banking App Page")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
class TestBankingAppPage:
    @allure.title("Successful registration")
    def test_registration_with_correct_data(
        self,
        banking_app_page: BankingAppPage,
        sample_form_page: SampleFormPage,
    ):
        banking_app_page.open_page()
        banking_app_page.click_sample_form_button()
        sample_form_page.page_is_opened()
        sample_form_page.enter_first_name(Faker().first_name())
        sample_form_page.enter_last_name(Faker().last_name())
        sample_form_page.enter_email(Faker().email())
        sample_form_page.enter_password(Faker().password())
        sample_form_page.select_sports_hobby()
        sample_form_page.select_gender("male")
        longest_hobby = max(sample_form_page.get_hobby_values(), key=len)
        sample_form_page.enter_about_yourself(
            f"The longest word from the suggested hobbies - {longest_hobby}"
        )
        sample_form_page.click_register_button()
        assert sample_form_page.is_success_message_displayed()

    @allure.title("Add customer")
    def test_add_customer(
        self,
        driver: WebDriver,
        customer: Customer,
    ):
        alert_text = _add_customer(driver, customer)
        assert "Customer added successfully" in alert_text, (
            f"Customer is not added: {alert_text}",
        )

    @allure.title("Open account")
    def test_open_account(
        self,
        driver: WebDriver,
        customer: Customer,
    ):
        _add_customer(driver, customer)
        alert_text = _open_account(driver, _customer_full_name(customer))
        assert "Account created successfully" in alert_text, (
            f"Account is not opened: {alert_text}",
        )

    @allure.title("Customer login")
    def test_customer_login(
        self,
        driver: WebDriver,
        customer: Customer,
    ):
        _add_customer(driver, customer)
        _open_account(driver, _customer_full_name(customer))
        customer_account_page = _login_as_customer(
            driver, _customer_full_name(customer)
        )
        message = customer_account_page.get_customer_welcome_message()
        assert message == _customer_full_name(customer), (
            f"Incorrect message: {message}"
        )

    @allure.title("Successful deposit")
    def test_deposit(
        self,
        logged_in_account: CustomerAccountPage,
    ):
        logged_in_account.click_deposit_button()
        logged_in_account.enter_amount("100")
        logged_in_account.click_submit_button()
        logged_in_account.wait_for_info_message("Deposit Successful")
        assert logged_in_account.get_info_message() == "Deposit Successful"
        logged_in_account.open_transactions_and_wait()
        logged_in_account.sort_transactions_by_date()
        assert logged_in_account.get_last_transaction() == ("Credit", "100")

    @allure.title("Failed deposit")
    def test_deposit_with_invalid_amount(
        self,
        logged_in_account: CustomerAccountPage,
    ):
        logged_in_account.click_deposit_button()
        logged_in_account.enter_amount("0")
        logged_in_account.click_submit_button()
        assert not logged_in_account.is_info_message_displayed()
        logged_in_account.enter_amount("100")
        logged_in_account.click_submit_button()
        logged_in_account.wait_for_info_message("Deposit Successful")
        logged_in_account.open_transactions_and_wait()
        logged_in_account.sort_transactions_by_date()
        assert logged_in_account.get_last_transaction() == ("Credit", "100")

    @allure.title("Successful withdraw")
    def test_withdraw(
        self,
        funded_account: CustomerAccountPage,
    ):
        funded_account.click_withdraw_button()
        funded_account.enter_amount("50")
        funded_account.click_submit_button()
        funded_account.wait_for_info_message("Transaction successful")
        assert funded_account.get_info_message() == "Transaction successful"
        funded_account.open_transactions_and_wait()
        funded_account.sort_transactions_by_date()
        assert funded_account.get_last_transaction() == ("Debit", "50")

    @allure.title("Failed withdraw")
    def test_withdraw_with_invalid_amount(
        self,
        logged_in_account: CustomerAccountPage,
    ):
        balance = logged_in_account.get_customer_balance()
        logged_in_account.click_withdraw_button()
        logged_in_account.enter_amount(str(int(balance) + 1))
        logged_in_account.click_submit_button()
        logged_in_account.wait_for_info_message("Transaction Failed")
        assert logged_in_account.get_info_message() == (
            "Transaction Failed. You can not withdraw amount more than the balance."
        )
        logged_in_account.click_deposit_button()
        logged_in_account.enter_amount("100")
        logged_in_account.click_submit_button()
        logged_in_account.wait_for_info_message("Deposit Successful")
        logged_in_account.open_transactions_and_wait()
        logged_in_account.sort_transactions_by_date()
        assert logged_in_account.get_last_transaction() == ("Credit", "100")

    @allure.title("Check balance")
    def test_check_balance(
        self,
        logged_in_account: CustomerAccountPage,
    ):
        logged_in_account.click_deposit_button()
        logged_in_account.enter_amount("100")
        logged_in_account.click_submit_button()
        logged_in_account.wait_for_info_message("Deposit Successful")
        logged_in_account.click_withdraw_button()
        logged_in_account.enter_amount("30")
        logged_in_account.click_submit_button()
        logged_in_account.wait_for_info_message("Transaction successful")
        balance = logged_in_account.get_customer_balance()
        assert balance == "70", f"Incorrect balance: {balance}"
        logged_in_account.open_transactions_and_wait()
        table_balance = _table_balance(
            logged_in_account.get_transaction_rows_text()
        )
        assert table_balance == int(balance), (
            f"Incorrect balance: {table_balance} != {balance}"
        )

    @allure.title("Withdraw all balance")
    def test_withdraw_all_balance(
        self,
        funded_account: CustomerAccountPage,
    ):
        balance = funded_account.get_customer_balance()
        funded_account.click_withdraw_button()
        funded_account.enter_amount(balance)
        funded_account.click_submit_button()
        funded_account.wait_for_info_message("Transaction successful")
        assert funded_account.get_info_message() == "Transaction successful"
        balance = funded_account.get_customer_balance()
        assert balance == "0", f"Balance is not 0: {balance}"

    @allure.title("Clear transactions history")
    def test_clear_transactions_history(
        self,
        funded_account: CustomerAccountPage,
    ):
        funded_account.open_transactions_and_wait()
        assert funded_account.get_transactions_count() > 0
        funded_account.click_reset_button()
        funded_account.wait_until_transactions_empty()
        funded_account.click_back_button()
        balance = funded_account.get_customer_balance()
        assert balance == "0", f"Balance is not 0: {balance}"

    @allure.title("Delete customer")
    def test_delete_customer(
        self,
        driver: WebDriver,
        bank_manager_login_page: BankManagerLoginPage,
        customers_page: CustomersPage,
        customer: Customer,
    ):
        _add_customer(driver, customer)
        bank_manager_login_page.open_page()
        bank_manager_login_page.click_customers_button()
        customers_page.enter_customer_name(customer.first_name)
        assert customers_page.is_delete_customer_button_displayed()
        customers_page.click_delete_customer_button()
        customers_page.clear_search_customer_field()
        assert customer.first_name not in customers_page.get_customers_names(), (
            f"Customer is not deleted: {customer.first_name}"
        )
