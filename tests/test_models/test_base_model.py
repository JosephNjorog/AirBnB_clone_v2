#!/usr/bin/python3
"""Unittests for BaseModel class"""
from models.base_model import BaseModel, Base
import unittest
import datetime
from uuid import UUID
import json
import os
from models import st_type


class TestBasemodel(unittest.TestCase):
    """Test case for BaseModel class"""

    def __init__(self, *args, **kwargs):
        """initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Set up test"""
        pass

    def tearDown(self):
        """End test"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """Test type"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test instances"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    @unittest.skipIf(
            st_type == 'db', 'DBStorage not supported')
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test __str__()"""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """Test to_dict()"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Tests if it's a dictionary
        self.assertIsInstance(self.value().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        self.assertNotIn('_sa_instance_state', self.value().to_dict())
        # Tests if to_dict contains added attributes
        mdl = self.value()
        mdl.firstname = 'Celestine'
        mdl.lastname = 'Akpanoko'
        self.assertIn('firstname', mdl.to_dict())
        self.assertIn('lastname', mdl.to_dict())
        self.assertIn('firstname', self.value(firstname='Celestine').to_dict())
        self.assertIn('lastname', self.value(lastname='Akpanoko').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        # Tests to_dict output contradiction
        mdl_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(mdl_d.to_dict(), mdl_d.__dict__)
        self.assertNotEqual(
            mdl_d.to_dict()['__class__'],
            mdl_d.__class__
        )

    def test_id(self):
        """Test ID"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test create_at"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    @unittest.skipIf(
            st_type == 'db', 'BaseModel not mapped in DBStorage')
    def test_updated_at(self):
        """Test updated_at"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)

    @unittest.skipIf(
        st_type == 'db', 'FileStorage test')
    def test_delete(self):
        """Tests the delete function of the BaseModel class."""
        from models import storage
        i = self.value()
        i.save()
        self.assertTrue(i in storage.all().values())
        i.delete()
        self.assertFalse(i in storage.all().values())
