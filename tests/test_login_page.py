import time

import allure
import pytest
from faker import Faker

from pages.login_page import LoginPage


@allure.epic("UI")
@allure.feature("Login page")
@pytest.mark.smoke
class TestLoginPage:
    @allure.story("Elements display")
    @allure.title("Input fields are displayed")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_fields_are_displayed(self, login_page: LoginPage):
        login_page.username_field_is_displayed()
        login_page.password_field_is_displayed()
        login_button_is_disabled = (
            login_page.find_login_button().get_attribute("disabled")
        )
        assert login_button_is_disabled == "true", \
            "Login button is not disabled"

    @allure.title("Login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_with_valid_credentials(self, login_page: LoginPage):
        login_page.enter_username_field("angular")
        login_page.enter_password_field("password")
        login_page.enter_username_description_field("angular")
        login_page.click_login_button()
        message = login_page.find_success_message()
        assert message.text == "You're logged in!!", \
            f"Incorrect message: {message.text}"

    @allure.title("Login with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_invalid_credentials(self, login_page: LoginPage):
        login_page.enter_username_field(Faker().user_name())
        login_page.enter_password_field(Faker().password())
        login_page.enter_username_description_field(Faker().user_name())
        login_page.click_login_button()
        message = login_page.find_error_message()
        assert message.text == "Username or password is incorrect", \
            f"Incorrect message: {message.text}"

    @allure.title("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, login_page: LoginPage):
        login_page.enter_username_field("angular")
        login_page.enter_password_field("password")
        login_page.enter_username_description_field("angular")
        login_page.click_login_button()
        login_page.click_logout_button()
        login_page.username_field_is_displayed()
        login_page.password_field_is_displayed()

    @allure.title("Login with various credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "credentials",
        [
            pytest.param(("angular", "password"), marks=pytest.mark.positive),
            pytest.param("wrong_credentials", marks=pytest.mark.negative)
        ],
        indirect=True
    )
    def test_login_with_various_credentials(
        self, login_page: LoginPage, credentials: tuple
    ):
        username, password = credentials
        login_page.enter_username_field(username)
        login_page.enter_password_field(password)
        login_page.enter_username_description_field(username)
        login_page.click_login_button()
        time.sleep(1)  # Successful login page does not have time to open
        if login_page.get_page_url() == login_page.URL:
            message = login_page.find_error_message()
            assert message.text == "Username or password is incorrect", \
                f"Incorrect message: {message.text}"
        else:
            message = login_page.find_success_message()
            assert message.text == "You're logged in!!", \
                f"Incorrect message: {message.text}"

    @allure.story("Elements display")
    @allure.title("Username description field title is displayed")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail
    def test_check_username_description_field_title(
        self, login_page: LoginPage
    ):
        title = login_page.find_username_description_field_title()
        assert title.text == "Username description", \
            f"Incorrect username description field title: \
                {title.text}"
