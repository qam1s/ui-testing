import allure
import pytest

from data.test_data import SQL_NICKNAME, SQL_PASSWORD, SQL_USERNAME
from pages.sql_page import SQLPage


@allure.epic("UI")
@allure.feature("SQL page")
@pytest.mark.smoke
class TestSQLPage:
    @allure.title("Authorization")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login(self, sql_page: SQLPage):
        sql_page.open_page()
        sql_page.enter_login(SQL_USERNAME)
        sql_page.enter_password(SQL_PASSWORD)
        sql_page.click_enter_button()
        nickname = sql_page.get_right_header_text()[-len(SQL_NICKNAME):]
        assert nickname == SQL_NICKNAME, f"Incorrect nickname: {nickname}"

    @allure.title("Session restore from cookie")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_session_restore_from_cookie(self, sql_page: SQLPage):
        sql_page.open_page()
        sql_page.enter_login(SQL_USERNAME)
        sql_page.enter_password(SQL_PASSWORD)
        sql_page.click_enter_button()
        session_cookie = sql_page.get_cookie("PHPSESSID")
        assert session_cookie is not None, "Session cookie is not set"
        sql_page.delete_cookie("PHPSESSID")
        sql_page.refresh_page()
        sql_page.add_cookie(session_cookie)
        sql_page.refresh_page()
        nickname = sql_page.get_right_header_text()[-len(SQL_NICKNAME):]
        assert nickname == SQL_NICKNAME, f"Incorrect nickname: {nickname}"

    @allure.title("Remove focus from Login field and check scroll presence")
    def test_remove_focus_from_login_field_and_check_scroll(
        self, sql_page: SQLPage
    ):
        sql_page.open_page()
        assert sql_page.is_login_field_displayed()
        assert sql_page.is_login_field_focused(), (
            "Login field is not focused"
        )
        sql_page.remove_focus()
        assert not sql_page.is_login_field_focused(), (
            "Login field is focused"
        )
        assert sql_page.page_is_scrollable(), "Page is not scrollable"
