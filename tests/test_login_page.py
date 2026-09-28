import allure
import pytest
from faker import Faker

from data.test_data import VALID_LOGIN_PASSWORD, VALID_LOGIN_USERNAME
from pages.login_page import LoginPage


@allure.epic("UI")
@allure.feature("Login page")
@pytest.mark.smoke
class TestLoginPage:
    @allure.story("Elements display")
    @allure.title("Input fields are displayed")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fields_are_displayed(self, login_page: LoginPage):
        login_page.open_page()
        assert login_page.is_username_field_displayed()
        assert login_page.is_password_field_displayed()
        assert login_page.is_login_button_disabled(), \
            "Login button is not disabled"

    @allure.title("Login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_valid_credentials(self, login_page: LoginPage):
        login_page.open_page()
        login_page.enter_username_field(VALID_LOGIN_USERNAME)
        login_page.enter_password_field(VALID_LOGIN_PASSWORD)
        login_page.enter_username_description_field(VALID_LOGIN_USERNAME)
        login_page.click_login_button()
        message = login_page.get_success_message()
        assert message == "You're logged in!!", \
            f"Incorrect message: {message}"

    @allure.title("Login with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_invalid_credentials(self, login_page: LoginPage):
        login_page.open_page()
        login_page.enter_username_field(Faker().user_name())
        login_page.enter_password_field(Faker().password())
        login_page.enter_username_description_field(Faker().user_name())
        login_page.click_login_button()
        message = login_page.get_error_message()
        assert message == "Username or password is incorrect", \
            f"Incorrect message: {message}"

    @allure.title("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, login_page: LoginPage):
        login_page.open_page()
        login_page.enter_username_field(VALID_LOGIN_USERNAME)
        login_page.enter_password_field(VALID_LOGIN_PASSWORD)
        login_page.enter_username_description_field(VALID_LOGIN_USERNAME)
        login_page.click_login_button()
        login_page.click_logout_button()
        assert login_page.is_username_field_displayed()
        assert login_page.is_password_field_displayed()

    @allure.title("Login with various credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "credentials",
        [
            pytest.param(
                (VALID_LOGIN_USERNAME, VALID_LOGIN_PASSWORD),
                marks=pytest.mark.positive,
            ),
            pytest.param("wrong_credentials", marks=pytest.mark.negative)
        ],
        indirect=True
    )
    def test_login_with_various_credentials(
        self, login_page: LoginPage, credentials: tuple
    ):
        username, password = credentials
        login_page.open_page()
        login_page.enter_username_field(username)
        login_page.enter_password_field(password)
        login_page.enter_username_description_field(username)
        login_page.click_login_button()
        outcome = login_page.wait_for_login_outcome()
        if outcome == "error":
            message = login_page.get_error_message()
            assert message == "Username or password is incorrect", \
                f"Incorrect message: {message}"
        else:
            message = login_page.get_success_message()
            assert message == "You're logged in!!", \
                f"Incorrect message: {message}"

    @allure.story("Elements display")
    @allure.title("Username description field title is displayed")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(
        reason="Demo site renders an unexpected username description title",
        strict=False,
    )
    def test_check_username_description_field_title(
        self, login_page: LoginPage
    ):
        login_page.open_page()
        title = login_page.get_username_description_field_title()
        assert title == "Username description", \
            f"Incorrect username description field title: {title}"
