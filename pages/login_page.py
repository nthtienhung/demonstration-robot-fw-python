"""
Login Page Object
Contains XPath locators and business methods for the Login Page
Follows POM pattern - NO selectors in test files
"""

from robot.api import logger
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Login Page Object for https://the-internet.herokuapp.com/login
    Contains all XPath locators and business methods for the login page
    """

    # ==================== XPath Locators ====================
    # All locators are XPath only - NO CSS selectors

    # Page Heading
    PAGE_HEADING = "//h2"
    SUB_HEADING = "//h4"

    # Form Elements
    USERNAME_INPUT = "//input[@id='username']"
    PASSWORD_INPUT = "//input[@id='password']"
    LOGIN_BUTTON = "//button[@type='submit']"

    # Messages
    FLASH_MESSAGE = "//div[@id='flash']"
    SUCCESS_MESSAGE = "//div[@id='flash' and contains(@class, 'success')]"
    ERROR_MESSAGE = "//div[@id='flash' and contains(@class, 'error')]"

    # Page Content
    USERNAME_LABEL = "//label[@for='username']"
    PASSWORD_LABEL = "//label[@for='password']"

    # Footer
    FOOTER = "//div[@id='page-footer']"
    POWERED_BY = "//div[@class='row']//div[contains(text(), 'Powered by')]"

    # Secure Page Elements (after successful login)
    SECURE_AREA_HEADING = "//h2"
    SECURE_AREA_MESSAGE = "//div[@class='flash success']"
    LOGOUT_BUTTON = "//a[@href='/logout']"
    WELCOME_MESSAGE = "//h4[contains(text(), 'Welcome')]"

    # ==================== Business Methods ====================

    def __init__(self, browser):
        """
        Initialize LoginPage with browser instance.

        Args:
            browser: SeleniumLibrary instance
        """
        super().__init__(browser)

    def get_page_heading(self) -> str:
        """
        Get the login page heading.

        Returns:
            Heading text content
        """
        heading = self.get_text(self.PAGE_HEADING)
        logger.info(f"Login page heading: {heading}")
        return heading

    def enter_username(self, username: str) -> None:
        """
        Enter username in the username field.

        Args:
            username: Username to enter
        """
        logger.info(f"Entering username: {username}")
        self.input_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """
        Enter password in the password field.

        Args:
            password: Password to enter
        """
        logger.info("Entering password")
        self.input_text(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Click the login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Perform login action with username and password.

        This is a business method representing the user action of logging in.
        Returns LoginPage (or SecurePage if implemented) for fluent chaining.

        Args:
            username: Username to use
            password: Password to use

        Returns:
            LoginPage instance (after login attempt)
        """
        logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

        # Wait for response
        self.browser.wait_until_element_is_visible(
            self.FLASH_MESSAGE,
            timeout="10s"
        )

        return self

    def get_flash_message(self) -> str:
        """
        Get the flash message text (success or error).

        Returns:
            Flash message text (with newlines cleaned)
        """
        try:
            message = self.get_text(self.FLASH_MESSAGE)
            # Clean up newlines and extra spaces
            message = ' '.join(message.split())
            logger.info(f"Flash message: {message}")
            return message
        except Exception:
            logger.warning("No flash message found")
            return ""

    def get_error_message(self) -> str:
        """
        Get the error message text.

        Returns:
            Error message text
        """
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout="5s")
            message = self.get_text(self.ERROR_MESSAGE)
            message = ' '.join(message.split())
            logger.info(f"Error message: {message}")
            return message
        except Exception:
            logger.warning("No error message found")
            return ""

    def is_login_successful(self) -> bool:
        """
        Check if login was successful.

        Returns:
            True if success message is visible, False otherwise
        """
        try:
            return self.is_element_present(self.SUCCESS_MESSAGE)
        except Exception:
            return False

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise
        """
        try:
            return self.is_element_present(self.ERROR_MESSAGE)
        except Exception:
            return False

    def get_secure_area_heading(self) -> str:
        """
        Get the secure area heading after successful login.

        Returns:
            Secure area heading text
        """
        try:
            self.wait_for_element(self.SECURE_AREA_HEADING, timeout="5s")
            heading = self.get_text(self.SECURE_AREA_HEADING)
            logger.info(f"Secure area heading: {heading}")
            return heading
        except Exception:
            logger.warning("Secure area heading not found")
            return ""

    def is_logout_button_visible(self) -> bool:
        """
        Check if logout button is visible (indicates successful login).

        Returns:
            True if logout button is visible, False otherwise
        """
        return self.is_element_present(self.LOGOUT_BUTTON)

    def logout(self) -> 'LoginPage':
        """
        Click logout button to log out.

        Returns:
            LoginPage instance
        """
        logger.info("Clicking logout button")
        self.click(self.LOGOUT_BUTTON)
        return self

    def get_username_placeholder(self) -> str:
        """
        Get the placeholder text of username field.

        Returns:
            Placeholder text
        """
        return self.get_attribute(self.USERNAME_INPUT, "placeholder")

    def get_password_placeholder(self) -> str:
        """
        Get the placeholder text of password field.

        Returns:
            Placeholder text
        """
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder")

    def is_username_field_visible(self) -> bool:
        """
        Check if username field is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_present(self.USERNAME_INPUT)

    def is_password_field_visible(self) -> bool:
        """
        Check if password field is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_present(self.PASSWORD_INPUT)

    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.

        Returns:
            True if enabled, False otherwise
        """
        return self.browser.element_should_be_enabled(
            self.LOGIN_BUTTON,
            message="Checking if login button is enabled"
        )

    def clear_credentials(self) -> None:
        """Clear both username and password fields."""
        logger.info("Clearing credentials")
        self.clear_and_input_text(self.USERNAME_INPUT, "")
        self.clear_and_input_text(self.PASSWORD_INPUT, "")

    def get_current_url(self) -> str:
        """
        Get the current URL.

        Returns:
            Current page URL
        """
        return super().get_current_url()
