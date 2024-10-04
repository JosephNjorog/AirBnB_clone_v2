#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import st_type

if st_type == 'db':
    from models.place import PlaceAmenity


class Amenity(BaseModel, Base):
    """represent amenities"""
    __tablename__ = 'amenities'
    name = Column(
            String(128), nullable=False
    ) if st_type == 'db' else ''
    if st_type == 'db':
        place_amenities = relationship(
                'Place',
                secondary=PlaceAmenity,
                back_populates='amenities',
        )
