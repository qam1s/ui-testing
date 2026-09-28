import os
from typing import Generator

import allure
import pytest
from dotenv import load_dotenv
from selenium.webdriver.remote.webdriver import WebDriver

from data.test_data import (
    VALID_LOGIN_PASSWORD,
    VALID_LOGIN_USERNAME,
    Credentials,
    Customer,
)
from pages.add_customer_page import AddCustomerPage
from pages.alert_page import AlertPage
from pages.authentication_page import AuthenticationPage
from pages.bank_manager_login_page import BankManagerLoginPage
from pages.banking_app_page import BankingAppPage
from pages.customer_account_page import CustomerAccountPage
from pages.customer_login_page import CustomerLoginPage
from pages.customers_page import CustomersPage
from pages.droppable_page import DroppablePage
from pages.frames_and_windows_page import FramesAndWindowsPage
from pages.lifetime_membership_page import LifetimeMembershipPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.open_account_page import OpenAccountPage
from pages.sample_form_page import SampleFormPage
from pages.sql_page import SQLPage
from utils.driver_factory import DriverFactory

load_dotenv()

DRIVER_KEY = pytest.StashKey[WebDriver]()


def _browsers() -> list[str]:
    raw = os.getenv("BROWSERS", "")
    browsers = [browser.strip() for browser in raw.split(",") if browser.strip()]
    return browsers or ["chrome"]


@pytest.fixture(scope="function", params=_browsers())
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    driver = DriverFactory.get_driver(browser=request.param)
    request.node.stash[DRIVER_KEY] = driver
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    if call.when == "call" and call.excinfo is not None:
        driver = item.stash.get(DRIVER_KEY, None)
        if driver is not None:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    "screenshot",
                    allure.attachment_type.PNG,
                )
            except Exception:
                pass


@pytest.fixture(scope="function")
def customer() -> Customer:
    return Customer()


@pytest.fixture
def credentials(request: pytest.FixtureRequest) -> tuple[str, str]:
    param = getattr(
        request, "param", (VALID_LOGIN_USERNAME, VALID_LOGIN_PASSWORD)
    )
    if param == "wrong_credentials":
        credentials = Credentials()
        return credentials.username, credentials.password
    return param


# pages


@pytest.fixture
def main_page(driver: WebDriver) -> MainPage:
    return MainPage(driver)


@pytest.fixture
def lifetime_membership_page(driver: WebDriver) -> LifetimeMembershipPage:
    return LifetimeMembershipPage(driver)


@pytest.fixture
def login_page(driver: WebDriver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def sql_page(driver: WebDriver) -> SQLPage:
    return SQLPage(driver)


@pytest.fixture
def droppable_page(driver: WebDriver) -> DroppablePage:
    return DroppablePage(driver)


@pytest.fixture
def frames_and_windows_page(driver: WebDriver) -> FramesAndWindowsPage:
    return FramesAndWindowsPage(driver)


@pytest.fixture
def alert_page(driver: WebDriver) -> AlertPage:
    return AlertPage(driver)


@pytest.fixture
def authentication_page(driver: WebDriver) -> AuthenticationPage:
    return AuthenticationPage(driver)


@pytest.fixture
def banking_app_page(driver: WebDriver) -> BankingAppPage:
    return BankingAppPage(driver)


@pytest.fixture
def sample_form_page(driver: WebDriver) -> SampleFormPage:
    return SampleFormPage(driver)


@pytest.fixture
def bank_manager_login_page(driver: WebDriver) -> BankManagerLoginPage:
    return BankManagerLoginPage(driver)


@pytest.fixture
def add_customer_page(driver: WebDriver) -> AddCustomerPage:
    return AddCustomerPage(driver)


@pytest.fixture
def open_account_page(driver: WebDriver) -> OpenAccountPage:
    return OpenAccountPage(driver)


@pytest.fixture
def customer_login_page(driver: WebDriver) -> CustomerLoginPage:
    return CustomerLoginPage(driver)


@pytest.fixture
def customer_account_page(driver: WebDriver) -> CustomerAccountPage:
    return CustomerAccountPage(driver)


@pytest.fixture
def customers_page(driver: WebDriver) -> CustomersPage:
    return CustomersPage(driver)
