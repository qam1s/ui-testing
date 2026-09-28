import allure
import pytest

from pages.main_page import MainPage
from pages.lifetime_membership_page import LifetimeMembershipPage

pytestmark = pytest.mark.skip(
    reason="way2automation.com was redesigned: the Astra-theme header, "
    "Most Popular Courses carousel and old footer no longer exist, "
    "so MainPage locators have nothing to match; "
    "MainPage needs a rebuild against the new static site"
)


@allure.epic("UI")
@allure.feature("Main page")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
class TestMainPage:
    @allure.title("Main page elements are displayed")
    def test_main_elements_are_displayed(self, main_page: MainPage):
        main_page.open_page()
        assert main_page.is_header_displayed()
        assert main_page.is_menu_displayed()
        assert main_page.is_reg_button_displayed()
        assert main_page.is_selenium_course_block_displayed()
        assert main_page.is_footer_displayed()

    @allure.title("Check header")
    def test_check_header(self, main_page: MainPage):
        main_page.open_page()
        contacts = main_page.get_header_text()
        for contact in main_page.HEADER_CONTACTS:
            assert contact in contacts, f"Contact {contact} is missing in header"

    @allure.title("Check navigation buttons in Most Popular Courses block")
    def test_check_most_popular_courses_block(self, main_page: MainPage):
        main_page.open_page()
        main_page.move_to_most_popular_courses_block()
        active_course_title = main_page.get_active_course_title()
        main_page.click_previous_most_popular_course_button()
        next_course_title = main_page.get_next_course_title()
        assert active_course_title == next_course_title, (
            "Back navigation button does not work"
        )
        main_page.open_page()
        main_page.move_to_most_popular_courses_block()
        active_course_title = main_page.get_active_course_title()
        main_page.click_next_most_popular_course_button()
        previous_course_title = main_page.get_previous_course_title()
        assert active_course_title == previous_course_title, (
            "Forward navigation button does not work"
        )

    @allure.title("Check footer")
    def test_check_footer(self, main_page: MainPage):
        main_page.open_page()
        contacts = main_page.get_footer_text()
        for contact in main_page.FOOTER_CONTACTS:
            assert contact in contacts, f"Contact {contact} is missing in footer"

    @allure.title("Menu is displayed after scrolling")
    def test_menu_is_displayed_after_scrolling(self, main_page: MainPage):
        main_page.open_page()
        main_page.scroll_to_bottom()
        assert main_page.is_menu_displayed()

    @allure.title("Navigate to Lifetime Membership page via All Courses menu")
    def test_click_lifetime_membership_button(
        self, main_page: MainPage, lifetime_membership_page: LifetimeMembershipPage
    ):
        main_page.open_page()
        main_page.click_lifetime_membership_button()
        lifetime_membership_page.page_is_opened()
        title = lifetime_membership_page.get_page_title()
        assert "LIFETIME MEMBERSHIP CLUB" in title, (
            f"Incorrect page title: {title}"
        )

    @allure.title("Check Lifetime Membership block")
    def test_check_lifetime_membership_block(self, main_page: MainPage):
        main_page.open_page()
        description = main_page.get_lifetime_membership_block_text()
        for keyword in ("LIFETIME MEMBERSHIP", "7000"):
            assert keyword in description, (
                f"Lifetime Membership block misses {keyword!r}: {description}"
            )
