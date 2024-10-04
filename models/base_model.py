#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base

from models import st_type

if st_type == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""

    if st_type == 'db':
        id = Column(
                String(60), nullable=False, primary_key=True, unique=True)
        created_at = Column(
                DATETIME, nullable=False, default=datetime.utcnow())
        updated_at = Column(
                DATETIME, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            if 'id' not in kwargs.keys():
                setattr(self, 'id', str(uuid.uuid4()))
            if 'created_at' not in kwargs.keys():
                setattr(self, 'created_at', datetime.now())
            if 'updated_at' not in kwargs.keys():
                setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        obj_dict = self.__dict__
        try:
            del obj_dict['_sa_instance_state']
        except KeyError:
            pass
        return '[{}] ({}) {}'.format(cls, self.id, obj_dict)

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        from models import storage
        storage.delete(self)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    dictionary[key] = value.isoformat()
                else:
                    dictionary[key] = value
        dictionary['__class__'] = self.__class__.__name__
        return dictionary
