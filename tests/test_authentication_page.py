import allure
import pytest

from data.test_data import (
    HTTPWATCH_PASSWORD,
    HTTPWATCH_USERNAME,
)
from pages.authentication_page import AuthenticationPage


@allure.epic("UI")
@allure.feature("Authentication page")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
class TestAuthenticationPage:
    @allure.title("Authentication")
    def test_authentication(self, authentication_page: AuthenticationPage):
        authentication_page.open_page()
        authentication_page.click_display_image_button()
        authentication_page.open_image_page(
            HTTPWATCH_USERNAME, HTTPWATCH_PASSWORD
        )
        assert authentication_page.is_authenticated_image_displayed()
        image_src = authentication_page.get_authenticated_image_src()
        assert f"{HTTPWATCH_USERNAME}:{HTTPWATCH_PASSWORD}" in image_src, (
            f"Incorrect image: {image_src}"
        )
