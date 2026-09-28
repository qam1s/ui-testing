import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class AuthenticationPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://www.httpwatch.com/httpgallery/authentication/#showExample10"
        self.DISPLAY_IMAGE_BUTTON = (By.ID, "displayImage")
        self.AUTHENTICATED_IMAGE = (By.TAG_NAME, "img")

    @allure.step("Click Display Image Button")
    def click_display_image_button(self) -> None:
        self.click(self.DISPLAY_IMAGE_BUTTON)

    @allure.step("Open Image Page")
    def open_image_page(self, username: str, password: str) -> None:
        self.driver.get(
            f"https://{username}:{password}@www.httpwatch.com/httpgallery/authentication/authenticatedimage/default.aspx"  # noqa
        )

    def get_authenticated_image_src(self) -> str:
        return str(
            self.find_element(self.AUTHENTICATED_IMAGE).get_attribute("src")
        )

    def is_authenticated_image_displayed(self) -> bool:
        return self.is_element_displayed(self.AUTHENTICATED_IMAGE)
