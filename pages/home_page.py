"""
Home Page Object
Contains XPath locators and business methods for the Home Page
Follows POM pattern - NO selectors in test files
"""

from robot.api import logger
from pages.base_page import BasePage
from pages.login_page import LoginPage


class HomePage(BasePage):
    """
    Home Page Object for https://the-internet.herokuapp.com
    Contains all XPath locators and business methods for the home page
    """

    # ==================== XPath Locators ====================
    # All locators are XPath only - NO CSS selectors

    HEADING = "//h1"
    SUB_HEADING = "//h2"
    PAGE_TITLE = "The Internet"

    # Available Examples Links
    FORM_AUTHENTICATION_LINK = "//a[@href='/login']"
    DROPDOWN_LINK = "//a[@href='/dropdown']"
    CHECKBOXES_LINK = "//a[@href='/checkboxes']"
    ADD_REMOVE_ELEMENTS_LINK = "//a[@href='/add_remove_elements']"

    # Content Area
    CONTENT_AREA = "//div[@class='example']"
    AVAILABLE_EXAMPLES_LIST = "//li/a"

    # Footer
    FOOTER_TEXT = "//div[@id='page-footer']"
    POWERED_BY_TEXT = "//div[contains(text(), 'Powered by')]"

    # ==================== Business Methods ====================

    def __init__(self, browser):
        """
        Initialize HomePage with browser instance.

        Args:
            browser: SeleniumLibrary instance
        """
        super().__init__(browser)

    def get_page_heading(self) -> str:
        """
        Get the main heading text of the home page.

        Returns:
            The heading text content
        """
        heading = self.get_text(self.HEADING)
        logger.info(f"Home page heading: {heading}")
        return heading

    def is_form_authentication_link_visible(self) -> bool:
        """
        Check if the Form Authentication link is visible.

        Returns:
            True if link is visible, False otherwise
        """
        return self.is_element_present(self.FORM_AUTHENTICATION_LINK)

    def navigate_to_login(self) -> LoginPage:
        """
        Navigate to the Login page by clicking Form Authentication link.

        Returns:
            LoginPage instance for fluent chaining
        """
        logger.info("Navigating to Login page")
        self.click(self.FORM_AUTHENTICATION_LINK)
        return LoginPage(self.browser)

    def navigate_to_dropdown(self) -> 'HomePage':
        """
        Navigate to the Dropdown page.

        Returns:
            HomePage instance (or new page object if implemented)
        """
        logger.info("Navigating to Dropdown page")
        self.click(self.DROPDOWN_LINK)
        return HomePage(self.browser)

    def navigate_to_checkboxes(self) -> 'HomePage':
        """
        Navigate to the Checkboxes page.

        Returns:
            HomePage instance (or new page object if implemented)
        """
        logger.info("Navigating to Checkboxes page")
        self.click(self.CHECKBOXES_LINK)
        return HomePage(self.browser)

    def get_all_available_links(self) -> list:
        """
        Get all available example links on the home page.

        Returns:
            List of link texts
        """
        links = self.browser.find_elements(self.AVAILABLE_EXAMPLES_LIST)
        link_texts = [link.text for link in links]
        logger.info(f"Found {len(link_texts)} available links")
        return link_texts

    def is_footer_visible(self) -> bool:
        """
        Check if the page footer is visible.

        Returns:
            True if footer is visible, False otherwise
        """
        return self.is_element_present(self.FOOTER_TEXT)

    def get_footer_text(self) -> str:
        """
        Get the footer text content.

        Returns:
            Footer text
        """
        return self.get_text(self.FOOTER_TEXT)

    def is_page_loaded(self) -> bool:
        """
        Verify the home page is properly loaded.

        Returns:
            True if page is loaded (heading visible), False otherwise
        """
        try:
            self.wait_for_element(self.HEADING, timeout="5s")
            heading = self.get_page_heading()
            return "Welcome to the-internet" in heading or heading.lower() == "the internet"
        except Exception as e:
            logger.error(f"Page load verification failed: {e}")
            return False

    def scroll_to_footer(self) -> None:
        """Scroll to the footer section of the page."""
        self.scroll_to_element(self.FOOTER_TEXT)

    def click_link_by_text(self, link_text: str) -> None:
        """
        Click a link by its visible text.

        Args:
            link_text: The visible text of the link to click
        """
        # XPath to find link by exact text
        locator = f"//a[text()='{link_text}']"
        logger.info(f"Clicking link: {link_text}")
        self.click(locator)

    def get_url(self) -> str:
        """
        Get the current URL.

        Returns:
            Current page URL
        """
        return self.get_current_url()
