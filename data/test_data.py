from dataclasses import dataclass, field

from faker import Faker


@dataclass
class Customer:
    first_name: str = field(default_factory=lambda: Faker().first_name())
    last_name: str = field(default_factory=lambda: Faker().last_name())
    post_code: str = field(default_factory=lambda: Faker().postcode())


@dataclass
class Credentials:
    username: str = field(default_factory=lambda: Faker().user_name())
    password: str = field(default_factory=lambda: Faker().password())


VALID_LOGIN_USERNAME = "angular"
VALID_LOGIN_PASSWORD = "password"

SQL_USERNAME = "losoxo@azuretechtalk."
SQL_PASSWORD = "losoxo@azuretechtalk.net"
SQL_NICKNAME = "losoxo@azuretechtalk"

HTTPWATCH_USERNAME = "httpwatch"
HTTPWATCH_PASSWORD = "httpwatch"

CURRENCIES = ("Dollar", "Pound", "Rupee")
GENDERS = ("male", "female", "other")
