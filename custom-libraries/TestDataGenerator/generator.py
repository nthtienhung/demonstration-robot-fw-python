"""
Test Data Generator
Robot Framework library for generating random test data using Faker
"""

import json
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from robot.api import logger
from faker import Faker


class TestDataGenerator:
    """
    Test data generation library using Faker.
    Provides Robot Framework keywords for generating various types of test data.
    """

    def __init__(self, locale: str = 'en_US'):
        """
        Initialize TestDataGenerator with locale.

        Args:
            locale: Locale for data generation (default: en_US)
        """
        self.faker = Faker(locale=locale)
        logger.info(f"TestDataGenerator initialized with locale: {locale}")

    def generate_random_user(self) -> Dict[str, str]:
        """
        Generate a complete random user profile.

        Returns:
            Dictionary with user details (first_name, last_name, email, etc.)
        """
        user = {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'email': self.faker.email(),
            'username': self.faker.user_name(),
            'password': self._generate_password(),
            'phone': self.faker.phone_number(),
            'address': self.faker.street_address(),
            'city': self.faker.city(),
            'state': self.faker.state(),
            'zip_code': self.faker.zipcode(),
            'country': self.faker.country(),
            'date_of_birth': self.faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            'ssn': self.faker.ssn(),
            'company': self.faker.company(),
            'job_title': self.faker.job(),
            'website': self.faker.url(),
        }
        logger.info(f"Generated random user: {user['username']}")
        return user

    def generate_email(self, domain: Optional[str] = None) -> str:
        """
        Generate a random email address.

        Args:
            domain: Optional domain for the email

        Returns:
            Email address string
        """
        username = self.faker.user_name()
        if domain:
            email = f"{username}@{domain}"
        else:
            email = self.faker.email()
        logger.info(f"Generated email: {email}")
        return email

    def generate_phone_number(self, country_code: str = "US") -> str:
        """
        Generate a random phone number.

        Args:
            country_code: Country code for phone format (default: US)

        Returns:
            Phone number string
        """
        if country_code == "US":
            phone = self.faker.phone_number()
        elif country_code == "UK":
            phone = self.faker.phone_number()
        else:
            phone = self.faker.phone_number()
        logger.info(f"Generated phone number: {phone}")
        return phone

    def generate_address(self) -> Dict[str, str]:
        """
        Generate a complete address.

        Returns:
            Dictionary with address components
        """
        address = {
            'street_address': self.faker.street_address(),
            'city': self.faker.city(),
            'state': self.faker.state(),
            'zip_code': self.faker.zipcode(),
            'country': self.faker.country(),
            'latitude': str(self.faker.latitude()),
            'longitude': str(self.faker.longitude())
        }
        logger.info(f"Generated address: {address['city']}, {address['state']}")
        return address

    def generate_username(self) -> str:
        """
        Generate a random username.

        Returns:
            Username string
        """
        username = self.faker.user_name()
        logger.info(f"Generated username: {username}")
        return username

    def generate_password(self, length: int = 12, include_symbols: bool = True) -> str:
        """
        Generate a random password.

        Args:
            length: Password length (default: 12)
            include_symbols: Include special characters (default: True)

        Returns:
            Password string
        """
        password = self._generate_password(length, include_symbols)
        logger.info(f"Generated password (length: {length})")
        return password

    def _generate_password(self, length: int = 12, include_symbols: bool = True) -> str:
        """Internal password generation method."""
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*"

        return ''.join(random.choice(chars) for _ in range(length))

    def generate_name(self) -> Dict[str, str]:
        """
        Generate a random name.

        Returns:
            Dictionary with first_name and last_name
        """
        name = {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'full_name': self.faker.name()
        }
        logger.info(f"Generated name: {name['full_name']}")
        return name

    def generate_company(self) -> str:
        """
        Generate a random company name.

        Returns:
            Company name string
        """
        company = self.faker.company()
        logger.info(f"Generated company: {company}")
        return company

    def generate_credit_card(self) -> Dict[str, str]:
        """
        Generate random credit card information.

        Returns:
            Dictionary with credit card details
        """
        card = {
            'card_number': self.faker.credit_card_number(card_type=None),
            'card_provider': self.faker.credit_card_provider(),
            'expiry_date': self.faker.credit_card_expire(),
            'cvv': self.faker.credit_card_security_code()
        }
        logger.info(f"Generated credit card: {card['card_provider']}")
        return card

    def generate_date(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """
        Generate a random date within a range.

        Args:
            start_date: Start date string (YYYY-MM-DD), defaults to today - 30 days
            end_date: End date string (YYYY-MM-DD), defaults to today + 30 days

        Returns:
            Date string in YYYY-MM-DD format
        """
        if not start_date:
            start = datetime.now() - timedelta(days=30)
        else:
            start = datetime.strptime(start_date, '%Y-%m-%d')

        if not end_date:
            end = datetime.now() + timedelta(days=30)
        else:
            end = datetime.strptime(end_date, '%Y-%m-%d')

        random_date = self.faker.date_between(start_date=start, end_date=end)
        logger.info(f"Generated date: {random_date}")
        return random_date.strftime('%Y-%m-%d')

    def generate_text(self, max_nb_chars: int = 200) -> str:
        """
        Generate random text.

        Args:
            max_nb_chars: Maximum number of characters

        Returns:
            Text string
        """
        text = self.faker.text(max_nb_chars=max_nb_chars)
        logger.info(f"Generated text ({len(text)} chars)")
        return text

    def generate_sentence(self, nb_words: int = 10) -> str:
        """
        Generate a random sentence.

        Args:
            nb_words: Number of words in sentence

        Returns:
            Sentence string
        """
        sentence = self.faker.sentence(nb_words=nb_words)
        logger.info(f"Generated sentence: {sentence}")
        return sentence

    def generate_paragraph(self, nb_sentences: int = 3) -> str:
        """
        Generate a random paragraph.

        Args:
            nb_sentences: Number of sentences in paragraph

        Returns:
            Paragraph string
        """
        paragraph = self.faker.paragraph(nb_sentences=nb_sentences)
        logger.info(f"Generated paragraph ({nb_sentences} sentences)")
        return paragraph

    def generate_url(self) -> str:
        """
        Generate a random URL.

        Returns:
            URL string
        """
        url = self.faker.url()
        logger.info(f"Generated URL: {url}")
        return url

    def generate_ipv4(self) -> str:
        """
        Generate a random IPv4 address.

        Returns:
            IPv4 address string
        """
        ip = self.faker.ipv4()
        logger.info(f"Generated IPv4: {ip}")
        return ip

    def generate_uuid(self) -> str:
        """
        Generate a random UUID.

        Returns:
            UUID string
        """
        uuid = self.faker.uuid4()
        logger.info(f"Generated UUID: {uuid}")
        return uuid

    def generate_product(self) -> Dict[str, Any]:
        """
        Generate random product information.

        Returns:
            Dictionary with product details
        """
        product = {
            'name': self.faker.word().capitalize() + ' ' + self.faker.word().capitalize(),
            'description': self.faker.sentence(),
            'price': round(random.uniform(10, 1000), 2),
            'sku': self.faker.uuid4()[:8].upper(),
            'quantity': random.randint(1, 100),
            'category': self.faker.word(),
            'manufacturer': self.faker.company()
        }
        logger.info(f"Generated product: {product['name']}")
        return product

    def generate_user_list(self, count: int = 5) -> List[Dict[str, str]]:
        """
        Generate a list of random users.

        Args:
            count: Number of users to generate

        Returns:
            List of user dictionaries
        """
        users = [self.generate_random_user() for _ in range(count)]
        logger.info(f"Generated {count} users")
        return users

    def get_test_data_from_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Get test data based on a predefined schema.
        Supports common schemas: user, address, credit_card, product, login.

        Args:
            schema_name: Name of the schema to use

        Returns:
            Dictionary with generated data
        """
        schemas = {
            'user': self.generate_random_user,
            'address': self.generate_address,
            'credit_card': self.generate_credit_card,
            'product': self.generate_product,
            'login': lambda: {
                'username': self.generate_username(),
                'password': self.generate_password()
            },
            'email': lambda: {'email': self.generate_email()},
            'name': self.generate_name,
            'company': lambda: {'company': self.generate_company()}
        }

        schema_func = schemas.get(schema_name.lower())
        if schema_func:
            return schema_func()
        else:
            logger.error(f"Unknown schema: {schema_name}")
            raise ValueError(f"Unknown schema: {schema_name}. Available: {list(schemas.keys())}")

    def generate_random_string(self, length: int = 10, prefix: str = "") -> str:
        """
        Generate a random string.

        Args:
            length: Length of string (excluding prefix)
            prefix: Optional prefix for the string

        Returns:
            Random string with prefix
        """
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        result = f"{prefix}{random_str}"
        logger.info(f"Generated random string: {result}")
        return result

    def generate_random_number(self, min_val: int = 1, max_val: int = 1000) -> int:
        """
        Generate a random number in range.

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Random integer
        """
        number = random.randint(min_val, max_val)
        logger.info(f"Generated random number: {number}")
        return number

    def generate_boolean(self) -> bool:
        """
        Generate a random boolean value.

        Returns:
            Random boolean
        """
        return random.choice([True, False])

    def generate_from_list(self, items: List[Any]) -> Any:
        """
        Select a random item from a list.

        Args:
            items: List of items to choose from

        Returns:
            Randomly selected item
        """
        if not items:
            raise ValueError("Cannot select from empty list")
        return random.choice(items)

    def save_test_data(self, data: Dict[str, Any], filename: str) -> str:
        """
        Save test data to JSON file.

        Args:
            data: Data dictionary to save
            filename: Name of the file

        Returns:
            Path to saved file
        """
        filepath = f"robot-tests/results/test-data/{filename}"
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved test data to: {filepath}")
        return filepath

    def load_test_data(self, filename: str) -> Dict[str, Any]:
        """
        Load test data from JSON file.

        Args:
            filename: Name of the file

        Returns:
            Loaded data dictionary
        """
        filepath = f"config/test-data/{filename}"
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded test data from: {filepath}")
            return data
        except FileNotFoundError:
            logger.error(f"Test data file not found: {filepath}")
            raise


# ==================== Robot Framework Library Functions ====================

def generate_random_user():
    """Robot Framework keyword: Generate random user."""
    return TestDataGenerator().generate_random_user()


def generate_email(domain=None):
    """Robot Framework keyword: Generate email address."""
    return TestDataGenerator().generate_email(domain)


def generate_phone_number(country_code="US"):
    """Robot Framework keyword: Generate phone number."""
    return TestDataGenerator().generate_phone_number(country_code)


def generate_address():
    """Robot Framework keyword: Generate address."""
    return TestDataGenerator().generate_address()


def generate_password(length=12):
    """Robot Framework keyword: Generate password."""
    return TestDataGenerator().generate_password(length)


def get_test_data_from_schema(schema_name):
    """Robot Framework keyword: Get data by schema."""
    return TestDataGenerator().get_test_data_from_schema(schema_name)
