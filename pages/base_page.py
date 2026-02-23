"""
Base Page Class
Provides common Selenium wrapper methods for all page objects
Follows POM pattern - contains NO test logic, only interaction methods
"""

import os
from typing import Optional
from robot.api import logger
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords, ElementKeywords


class BasePage:
    """
    Base page class containing common Selenium interaction methods.
    All page objects inherit from this class.
    """

    def __init__(self, browser: SeleniumLibrary):
        """
        Initialize BasePage with SeleniumLibrary browser instance.

        Args:
            browser: SeleniumLibrary instance
        """
        self.browser = browser
        self._bm_keywords = BrowserManagementKeywords(browser)
        self._el_keywords = ElementKeywords(browser)

    def open_url(self, url: str) -> None:
        """
        Navigate to the specified URL.

        Args:
            url: The URL to navigate to
        """
        self.browser.go_to(url)
        logger.info(f"Navigated to: {url}")

    def click(self, locator: str) -> None:
        """
        Click on an element identified by locator.

        Args:
            locator: XPath locator string
        """
        self.browser.click_element(locator)
        logger.info(f"Clicked element: {locator}")

    def input_text(self, locator: str, text: str) -> None:
        """
        Input text into a field.

        Args:
            locator: XPath locator string
            text: Text to input
        """
        self.browser.input_text(locator, text)
        logger.info(f"Entered text into: {locator}")

    def clear_and_input_text(self, locator: str, text: str) -> None:
        """
        Clear field and input text.

        Args:
            locator: XPath locator string
            text: Text to input
        """
        self.browser.clear_element_text(locator)
        self.browser.input_text(locator, text)
        logger.info(f"Cleared and entered text into: {locator}")

    def get_text(self, locator: str) -> str:
        """
        Get text content of an element.

        Args:
            locator: XPath locator string

        Returns:
            Text content of the element
        """
        text = self.browser.get_text(locator)
        logger.info(f"Retrieved text from: {locator}")
        return text

    def get_attribute(self, locator: str, attribute: str) -> str:
        """
        Get attribute value of an element.

        Args:
            locator: XPath locator string
            attribute: Attribute name to retrieve

        Returns:
            Attribute value
        """
        value = self.browser.get_element_attribute(locator, attribute)
        logger.info(f"Retrieved attribute '{attribute}' from: {locator}")
        return value

    def is_visible(self, locator: str) -> bool:
        """
        Check if element is visible.

        Args:
            locator: XPath locator string

        Returns:
            True if element is visible, False otherwise
        """
        visible = self.browser.element_should_be_visible(
            locator,
            message=f"Checking visibility of: {locator}"
        )
        return visible

    def is_element_present(self, locator: str) -> bool:
        """
        Check if element is present in DOM.

        Args:
            locator: XPath locator string

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.browser.get_webelement(locator)
            return True
        except Exception:
            return False

    def wait_for_element(self, locator: str, timeout: str = "10s") -> None:
        """
        Wait for element to be visible.

        Args:
            locator: XPath locator string
            timeout: Timeout duration (e.g., "10s")
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)
        logger.info(f"Element visible after wait: {locator}")

    def wait_for_element_clickable(self, locator: str, timeout: str = "10s") -> None:
        """
        Wait for element to be clickable.

        Args:
            locator: XPath locator string
            timeout: Timeout duration (e.g., "10s")
        """
        self.browser.wait_until_element_is_enabled(locator, timeout=timeout)
        logger.info(f"Element clickable after wait: {locator}")

    def wait_for_page_load(self, timeout: str = "30s") -> None:
        """
        Wait for page to complete loading.

        Args:
            timeout: Timeout duration (e.g., "30s")
        """
        self.browser.wait_for_page_load(timeout)

    def capture_screenshot(self, name: str) -> str:
        """
        Capture screenshot of current page.

        Args:
            name: Name for the screenshot file

        Returns:
            Path to the captured screenshot
        """
        # Ensure screenshot directory exists
        screenshot_dir = "robot-tests/results/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.browser.capture_page_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def capture_element_screenshot(self, locator: str, name: str) -> str:
        """
        Capture screenshot of specific element.

        Args:
            locator: XPath locator string
            name: Name for the screenshot file

        Returns:
            Path to the captured screenshot
        """
        screenshot_dir = "robot-tests/results/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.browser.capture_element_screenshot(locator, screenshot_path)
        logger.info(f"Element screenshot saved: {screenshot_path}")
        return screenshot_path

    def scroll_to_element(self, locator: str) -> None:
        """
        Scroll to make element visible.

        Args:
            locator: XPath locator string
        """
        self.browser.scroll_element_into_view(locator)
        logger.info(f"Scrolled to element: {locator}")

    def select_from_dropdown_by_label(self, locator: str, label: str) -> None:
        """
        Select option from dropdown by visible text.

        Args:
            locator: XPath locator string
            label: Visible text of option to select
        """
        self.browser.select_from_list_by_label(locator, label)
        logger.info(f"Selected '{label}' from dropdown: {locator}")

    def select_from_dropdown_by_value(self, locator: str, value: str) -> None:
        """
        Select option from dropdown by value attribute.

        Args:
            locator: XPath locator string
            value: Value attribute of option to select
        """
        self.browser.select_from_list_by_value(locator, value)
        logger.info(f"Selected value '{value}' from dropdown: {locator}")

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title
        """
        title = self.browser.get_title()
        logger.info(f"Page title: {title}")
        return title

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL
        """
        url = self.browser.get_location()
        logger.info(f"Current URL: {url}")
        return url

    def switch_to_frame(self, locator: str) -> None:
        """
        Switch to iframe.

        Args:
            locator: XPath locator string for the iframe
        """
        self.browser.select_frame(locator)
        logger.info(f"Switched to frame: {locator}")

    def switch_to_default_content(self) -> None:
        """Switch back to main document from iframe."""
        self.browser.unselect_frame()
        logger.info("Switched to default content")

    def execute_javascript(self, script: str) -> any:
        """
        Execute JavaScript in the browser.

        Args:
            script: JavaScript code to execute

        Returns:
            Result of JavaScript execution
        """
        result = self.browser.execute_javascript(script)
        logger.info(f"Executed JavaScript: {script[:50]}...")
        return result

    def hover_over_element(self, locator: str) -> None:
        """
        Hover mouse over element.

        Args:
            locator: XPath locator string
        """
        self.browser.mouse_over(locator)
        logger.info(f"Hovered over element: {locator}")

    def double_click(self, locator: str) -> None:
        """
        Double click on element.

        Args:
            locator: XPath locator string
        """
        self.browser.double_click_element(locator)
        logger.info(f"Double clicked element: {locator}")

    def right_click(self, locator: str) -> None:
        """
        Right click on element.

        Args:
            locator: XPath locator string
        """
        self.browser.open_context_menu(locator)
        logger.info(f"Right clicked element: {locator}")
