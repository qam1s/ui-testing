import allure
import pytest

from pages.frames_and_windows_page import FramesAndWindowsPage


@allure.epic("UI")
@allure.feature("Frames and windows page")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
class TestFramesAndWindowsPage:
    @allure.title("Open new browser tab")
    def test_open_new_browser_tab(
        self, frames_and_windows_page: FramesAndWindowsPage
    ):
        frames_and_windows_page.open_page()
        frames_and_windows_page.switch_to_frame()
        try:
            for _ in range(2):
                windows = frames_and_windows_page.get_all_windows()
                frames_and_windows_page.click_new_browser_tab_link()
                frames_and_windows_page.wait_for_windows_count(len(windows) + 1)
                windows_after_click = frames_and_windows_page.get_all_windows()
                frames_and_windows_page.switch_to_window(windows_after_click[-1])
                assert frames_and_windows_page.is_new_browser_tab_link_displayed()
        finally:
            frames_and_windows_page.close_extra_windows()
            frames_and_windows_page.switch_to_default_content()
