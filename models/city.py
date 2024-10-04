#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import st_type


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    name = Column(
        String(128), nullable=False
    ) if st_type == 'db' else ''
    state_id = Column(
        String(60), ForeignKey('states.id'), nullable=False
    ) if st_type == 'db' else ''
    if st_type == 'db':
        state = relationship(
            'State',
            back_populates='cities'
        )
        places = relationship(
            'Place',
            cascade='all, delete, delete-orphan',
            back_populates='cities'
        )
