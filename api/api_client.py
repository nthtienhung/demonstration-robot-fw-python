"""
API Client
REST API wrapper for making HTTP requests
Provides convenient methods for API testing
"""

import json
import yaml
from typing import Optional, Dict, Any
from robot.api import logger
import requests
from requests.exceptions import RequestException


class APIClient:
    """
    REST API client wrapper using requests library.
    Provides convenient methods for common HTTP operations.
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize API client with configuration.

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.base_url = self.config.get('api', {}).get(
            'base_url', 'https://jsonplaceholder.typicode.com'
        )
        self.timeout = self.config.get('api', {}).get('timeout', 30)
        self.session = requests.Session()
        self.last_response = None

        logger.info(f"API Client initialized with base URL: {self.base_url}")

    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warn(f"Config file not found: {config_path}")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config: {e}")
            return {}

    def set_base_url(self, url: str) -> None:
        """
        Set base URL for API requests.

        Args:
            url: Base URL
        """
        self.base_url = url
        logger.info(f"Base URL set to: {url}")

    def set_auth_header(self, token: str, auth_type: str = "Bearer") -> None:
        """
        Set authorization header.

        Args:
            token: Auth token
            auth_type: Type of auth (Bearer, Basic, etc.)
        """
        self.session.headers.update({
            'Authorization': f"{auth_type} {token}"
        })
        logger.info(f"Authorization header set: {auth_type}")

    def set_header(self, key: str, value: str) -> None:
        """
        Set a custom header.

        Args:
            key: Header name
            value: Header value
        """
        self.session.headers.update({key: value})
        logger.info(f"Header set: {key}")

    def clear_headers(self) -> None:
        """Clear all custom headers."""
        self.session.headers.clear()
        logger.info("All headers cleared")

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Full URL
        """
        # Remove leading slash if present and add it
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Perform GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        logger.info(f"GET request to: {url}")

        try:
            self.last_response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            logger.info(f"Response status: {self.last_response.status_code}")
            return self.last_response
        except RequestException as e:
            logger.error(f"GET request failed: {e}")
            raise

    def post(self, endpoint: str, data: Optional[Dict] = None,
             json_data: Optional[Dict] = None) -> requests.Response:
        """
        Perform POST request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        logger.info(f"POST request to: {url}")

        try:
            self.last_response = self.session.post(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            logger.info(f"Response status: {self.last_response.status_code}")
            return self.last_response
        except RequestException as e:
            logger.error(f"POST request failed: {e}")
            raise

    def put(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None) -> requests.Response:
        """
        Perform PUT request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        logger.info(f"PUT request to: {url}")

        try:
            self.last_response = self.session.put(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            logger.info(f"Response status: {self.last_response.status_code}")
            return self.last_response
        except RequestException as e:
            logger.error(f"PUT request failed: {e}")
            raise

    def patch(self, endpoint: str, data: Optional[Dict] = None,
              json_data: Optional[Dict] = None) -> requests.Response:
        """
        Perform PATCH request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        logger.info(f"PATCH request to: {url}")

        try:
            self.last_response = self.session.patch(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            logger.info(f"Response status: {self.last_response.status_code}")
            return self.last_response
        except RequestException as e:
            logger.error(f"PATCH request failed: {e}")
            raise

    def delete(self, endpoint: str) -> requests.Response:
        """
        Perform DELETE request.

        Args:
            endpoint: API endpoint

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        logger.info(f"DELETE request to: {url}")

        try:
            self.last_response = self.session.delete(
                url,
                timeout=self.timeout
            )
            logger.info(f"Response status: {self.last_response.status_code}")
            return self.last_response
        except RequestException as e:
            logger.error(f"DELETE request failed: {e}")
            raise

    def get_json(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Perform GET request and return JSON response.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            JSON response as dictionary
        """
        response = self.get(endpoint, params)
        response.raise_for_status()
        return response.json()

    def post_json(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Perform POST request and return JSON response.

        Args:
            endpoint: API endpoint
            data: JSON data to send

        Returns:
            JSON response as dictionary
        """
        response = self.post(endpoint, json_data=data)
        response.raise_for_status()
        return response.json()

    def assert_status_code(self, expected_status: int,
                           actual_response: Optional[requests.Response] = None) -> bool:
        """
        Assert response status code.

        Args:
            expected_status: Expected status code
            actual_response: Response object (uses last_response if None)

        Returns:
            True if status codes match
        """
        response = actual_response or self.last_response
        if response is None:
            raise ValueError("No response available to check status code")

        actual = response.status_code
        if actual == expected_status:
            logger.info(f"Status code assertion passed: {actual}")
            return True
        else:
            logger.error(f"Status code mismatch: expected {expected_status}, got {actual}")
            raise AssertionError(f"Expected status {expected_status}, got {actual}")

    def assert_response_contains_key(self, key: str,
                                      response: Optional[requests.Response] = None) -> bool:
        """
        Assert JSON response contains a specific key.

        Args:
            key: Key to check for
            response: Response object (uses last_response if None)

        Returns:
            True if key exists in response
        """
        response = response or self.last_response
        if response is None:
            raise ValueError("No response available")

        data = response.json()
        if key in data:
            logger.info(f"Response contains key: {key}")
            return True
        else:
            raise AssertionError(f"Response does not contain key: {key}")

    def get_response_time(self) -> float:
        """
        Get response time of last request in milliseconds.

        Returns:
            Response time in milliseconds
        """
        if self.last_response is None:
            raise ValueError("No response available")
        return self.last_response.elapsed.total_seconds() * 1000

    def get_last_response(self) -> Optional[requests.Response]:
        """
        Get the last response object.

        Returns:
            Last response object or None
        """
        return self.last_response

    def close(self) -> None:
        """Close the session."""
        self.session.close()
        logger.info("API session closed")


# ==================== Robot Framework Library Functions ====================

def create_api_session():
    """
    Robot Framework keyword: Create new API session.

    Returns:
        APIClient instance
    """
    return APIClient()


def get_api_base_url():
    """
    Robot Framework keyword: Get API base URL.

    Returns:
        Base URL string
    """
    client = APIClient()
    return client.base_url


def api_get(endpoint, params=None):
    """
    Robot Framework keyword: Perform API GET request.

    Args:
        endpoint: API endpoint
        params: Query parameters (as dict)

    Returns:
        JSON response
    """
    client = APIClient()
    return client.get(endpoint, params)


def api_post(endpoint, data=None):
    """
    Robot Framework keyword: Perform API POST request.

    Args:
        endpoint: API endpoint
        data: JSON data (as dict)

    Returns:
        JSON response
    """
    client = APIClient()
    return client.post(endpoint, json_data=data)
