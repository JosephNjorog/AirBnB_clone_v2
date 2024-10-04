#!/usr/bin/python3
""" Test case for user class """
from sqlalchemy import Column
from tests.test_models.test_base_model import TestBasemodel
from models.user import User
from models import st_type


class TestUser(TestBasemodel):
    """Represents the tests for the User model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Tests the type of first_name."""
        new = self.value()
        self.assertEqual(
            type(new.first_name),
            str if st_type != 'db' else type(None)
        )

    def test_last_name(self):
        """Tests the type of last_name."""
        new = self.value()
        self.assertEqual(
            type(new.last_name),
            str if st_type != 'db' else type(None)
        )

    def test_email(self):
        """Tests the type of email."""
        new = self.value()
        self.assertEqual(
            type(new.email),
            str if st_type != 'db' else type(None)
        )

    def test_password(self):
        """Tests the type of password."""
        new = self.value()
        self.assertEqual(
            type(new.password),
            str if st_type != 'db' else type(None)
        )
