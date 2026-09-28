import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class DroppablePage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.URL = "https://way2automation.com/way2auto_jquery/droppable.php"
        self.IFRAME = (By.XPATH, "//iframe[@class='demo-frame']")
        self.DRAGGABLE_ELEMENT = (By.ID, "draggable")
        self.DROPPABLE_ELEMENT = (By.ID, "droppable")

    def switch_to_frame(self) -> None:
        self.driver.switch_to.frame(self.find_element(self.IFRAME))

    def get_droppable_text(self) -> str:
        return self.find_element(self.DROPPABLE_ELEMENT).text

    @allure.step("Drag and drop element")
    def drag_and_drop_element(self) -> None:
        self.action.drag_and_drop(
            self.find_element(self.DRAGGABLE_ELEMENT),
            self.find_element(self.DROPPABLE_ELEMENT),
        ).perform()
