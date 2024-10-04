#!/usr/bin/python3
"""This module defines a class User"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import st_type


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(
        String(128), nullable=False
    ) if st_type == 'db' else ''
    password = Column(
        String(128), nullable=False
    ) if st_type == 'db' else ''
    first_name = Column(
        String(128)
    ) if st_type == 'db' else ''
    last_name = Column(
        String(128)
    ) if st_type == 'db' else ''
    if st_type == 'db':
        places = relationship(
            'Place',
            cascade='all, delete, delete-orphan',
            back_populates='user'
        )
        reviews = relationship(
            'Review',
            cascade='all, delete, delete-orphan',
            back_populates='user'
        )
