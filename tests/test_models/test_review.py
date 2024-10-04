#!/usr/bin/python3
""" Test case for Review class """
from tests.test_models.test_base_model import TestBasemodel
from models.review import Review
from models import st_type


class TestReview(TestBasemodel):
    """ review test class"""

    def __init__(self, *args, **kwargs):
        """ review class init"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ testing review place_id attr"""
        new = self.value()
        self.assertEqual(type(new.place_id), str if
                         st_type != 'db' else
                         type(None))

    def test_user_id(self):
        """ testing review user_id attr"""
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         st_type != 'db' else
                         type(None))

    def test_text(self):
        """ testing review text attr"""
        new = self.value()
        self.assertEqual(type(new.text), str if
                         st_type != 'db' else
                         type(None))
