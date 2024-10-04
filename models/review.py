#!/usr/bin/python3
""" Review module for the HBNB project """
import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import st_type


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    text = Column(
            String(1024), nullable=False
    ) if st_type == 'db' else ''
    place_id = Column(
            String(60), ForeignKey('places.id'), nullable=False
    ) if st_type == 'db' else ''
    user_id = Column(
            String(60), ForeignKey('users.id'), nullable=False
    ) if st_type == 'db' else ''
    if st_type == 'db':
        user = relationship(
                'User',
                back_populates='reviews'
        )
        place = relationship(
                'Place',
                back_populates='reviews'
        )
