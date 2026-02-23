"""
Page Factory Class
Factory pattern implementation to instantiate page objects
Manages browser lifecycle and provides page object instances
"""

import yaml
import os
from typing import Optional
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import BrowserManagementKeywords

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.base_page import BasePage


class PageFactory:
    """
    Factory class for creating and managing page objects.
    Handles browser initialization and provides page instances.
    """

    _browser: Optional[SeleniumLibrary] = None
    _config: dict = {}

    @classmethod
    def load_config(cls, config_path: str = "config/config.yaml") -> dict:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                cls._config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from: {config_path}")
            return cls._config
        except FileNotFoundError:
            logger.warn(f"Config file not found: {config_path}, using defaults")
            return cls._get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            return cls._get_default_config()

    @classmethod
    def _get_default_config(cls) -> dict:
        """Get default configuration."""
        return {
            'ui': {
                'base_url': 'https://the-internet.herokuapp.com',
                'browser': 'chrome',
                'headless': True,
                'timeout': '10s',
                'screenshot_on_failure': True
            },
            'api': {
                'base_url': 'https://jsonplaceholder.typicode.com',
                'timeout': '30s'
            }
        }

    @classmethod
    def get_config(cls) -> dict:
        """
        Get loaded configuration.

        Returns:
            Configuration dictionary
        """
        if not cls._config:
            cls.load_config()
        return cls._config

    @classmethod
    def get_ui_config(cls) -> dict:
        """
        Get UI configuration section.

        Returns:
            UI configuration dictionary
        """
        return cls.get_config().get('ui', {})

    @classmethod
    def get_api_config(cls) -> dict:
        """
        Get API configuration section.

        Returns:
            API configuration dictionary
        """
        return cls.get_config().get('api', {})

    @classmethod
    def get_base_url(cls) -> str:
        """
        Get base URL from configuration.

        Returns:
            Base URL
        """
        return cls.get_ui_config().get('base_url', 'https://the-internet.herokuapp.com')

    @classmethod
    def get_browser_name(cls) -> str:
        """
        Get browser name from configuration.

        Returns:
            Browser name (chrome, firefox, etc.)
        """
        return cls.get_ui_config().get('browser', 'chrome')

    @classmethod
    def is_headless(cls) -> bool:
        """
        Get headless mode from configuration.

        Returns:
            True if headless mode is enabled
        """
        return cls.get_ui_config().get('headless', False)

    @classmethod
    def init_browser(cls, browser: Optional[str] = None,
                     headless: Optional[bool] = None,
                     url: Optional[str] = None) -> SeleniumLibrary:
        """
        Initialize browser instance.

        Args:
            browser: Browser name (chrome, firefox, edge). If None, uses config
            headless: Headless mode. If None, uses config
            url: Initial URL to navigate to. If None, uses base_url from config

        Returns:
            SeleniumLibrary instance
        """
        if cls._browser is None:
            config = cls.get_config()
            ui_config = config.get('ui', {})

            browser = browser or cls.get_browser_name()
            headless = headless if headless is not None else cls.is_headless()

            # Create SeleniumLibrary instance
            cls._browser = SeleniumLibrary()

            # Setup browser with options
            options = cls._get_browser_options(browser, headless)

            # Open browser
            base_url = url or cls.get_base_url()
            cls._browser.open_browser(
                url=base_url,
                browser=browser,
                options=options
            )

            # Set implicit wait
            timeout = ui_config.get('implicit_wait', '5s')
            cls._browser.set_selenium_timeout(timeout)
            cls._browser.set_selenium_implicit_wait(timeout)

            # Maximize window if not headless
            if not headless:
                cls._browser.maximize_browser_window()

            logger.info(f"Browser initialized: {browser}, headless={headless}")

        return cls._browser

    @classmethod
    def _get_browser_options(cls, browser: str, headless: bool) -> str:
        """
        Get browser options string for SeleniumLibrary.

        Args:
            browser: Browser name
            headless: Headless mode

        Returns:
            Options string
        """
        if browser.lower() == 'chrome':
            options = []
            if headless:
                options.append('headless=new')
            if options:
                return 'add_argument:' + ';add_argument:'.join(options)
        return ''

    @classmethod
    def close_browser(cls) -> None:
        """Close browser instance."""
        if cls._browser is not None:
            cls._browser.close_all_browsers()
            cls._browser = None
            logger.info("Browser closed")

    @classmethod
    def get_browser(cls) -> Optional[SeleniumLibrary]:
        """
        Get existing browser instance or initialize new one.

        Returns:
            SeleniumLibrary instance
        """
        if cls._browser is None:
            return cls.init_browser()
        return cls._browser

    @classmethod
    def get_home_page(cls, url: Optional[str] = None) -> HomePage:
        """
        Get HomePage instance.

        Args:
            url: URL to navigate to. If None, uses base_url

        Returns:
            HomePage instance
        """
        browser = cls.get_browser()
        if url:
            browser.go_to(url)
        else:
            base_url = cls.get_base_url()
            if browser.get_location() != base_url:
                browser.go_to(base_url)
        return HomePage(browser)

    @classmethod
    def get_login_page(cls) -> LoginPage:
        """
        Get LoginPage instance.
        Navigates to login page first.

        Returns:
            LoginPage instance
        """
        browser = cls.get_browser()
        base_url = cls.get_base_url()
        browser.go_to(f"{base_url}/login")
        return LoginPage(browser)

    @classmethod
    def get_current_page(cls) -> BasePage:
        """
        Determine current page and return appropriate page object.

        Returns:
            Appropriate page object based on current URL
        """
        browser = cls.get_browser()
        url = browser.get_location()

        if '/login' in url:
            return LoginPage(browser)
        else:
            return HomePage(browser)

    # ==================== Robot Framework Keywords ====================

    @classmethod
    def open_browser_and_navigate_to_home(cls) -> HomePage:
        """
        Robot Framework keyword to open browser and navigate to home page.

        Returns:
            HomePage instance
        """
        return cls.get_home_page()

    @classmethod
    def open_browser_and_navigate_to_login(cls) -> LoginPage:
        """
        Robot Framework keyword to open browser and navigate to login page.

        Returns:
            LoginPage instance
        """
        return cls.get_login_page()

    @classmethod
    def close_all_browsers(cls) -> None:
        """Robot Framework keyword to close all browsers."""
        cls.close_browser()

    @classmethod
    def capture_screenshot(cls, name: str) -> str:
        """
        Capture screenshot using current browser.

        Args:
            name: Screenshot name

        Returns:
            Path to screenshot file
        """
        browser = cls.get_browser()
        return browser.capture_page_screenshot(f"robot-tests/results/screenshots/{name}.png")


# ==================== Robot Framework Library Functions ====================
# These functions are exposed as keywords in Robot Framework tests

def get_home_page(url=None):
    """
    Robot Framework keyword: Get HomePage instance.

    Args:
        url: Optional URL to navigate to

    Returns:
        HomePage instance
    """
    return PageFactory.get_home_page(url)


def get_login_page():
    """
    Robot Framework keyword: Get LoginPage instance.

    Returns:
        LoginPage instance
    """
    return PageFactory.get_login_page()


def open_browser():
    """
    Robot Framework keyword: Initialize browser.

    Returns:
        SeleniumLibrary instance
    """
    return PageFactory.init_browser()


def close_browser():
    """Robot Framework keyword: Close browser."""
    PageFactory.close_browser()


def get_base_url():
    """
    Robot Framework keyword: Get base URL from config.

    Returns:
        Base URL string
    """
    return PageFactory.get_base_url()
