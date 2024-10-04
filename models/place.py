#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import st_type


if st_type == 'db':
    PlaceAmenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True, nullable=False)
    )


class Place(BaseModel, Base):
    """ A place to stay """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amenity_ids = []

    __tablename__ = 'places'
    city_id = Column(
        String(60), ForeignKey('cities.id'), nullable=False
    ) if st_type == 'db' else ''
    user_id = Column(
        String(60), ForeignKey('users.id'), nullable=False
    ) if st_type == 'db' else ''
    name = Column(
        String(128), nullable=False
    ) if st_type == 'db' else ''
    description = Column(
        String(1024)
    ) if st_type == 'db' else ''
    number_rooms = Column(
        Integer, nullable=False, default=0
    ) if st_type == 'db' else 0
    number_bathrooms = Column(
        Integer, nullable=False, default=0
    ) if st_type == 'db' else 0
    max_guest = Column(
        Integer, nullable=False, default=0
    ) if st_type == 'db' else 0
    price_by_night = Column(
        Integer, nullable=False, default=0
    ) if st_type == 'db' else 0
    latitude = Column(
        Float
    ) if st_type == 'db' else 0.0
    longitude = Column(
        Float
    ) if st_type == 'db' else 0.0
    if st_type == 'db':
        user = relationship(
                'User',
                back_populates='places'
        )
        cities = relationship(
                'City',
                back_populates='places'
        )
        reviews = relationship(
                'Review',
                cascade='all, delete, delete-orphan',
                back_populates='place'
        )
        amenities = relationship(
                'Amenity',
                secondary=PlaceAmenity,
                back_populates='place_amenities',
                viewonly=False
        )
    else:
        @property
        def reviews(self):
            """returns the list of Review instances
            of specific place
            """
            from models import storage
            from model.review import Review
            reviews_objs = []
            for v in storage.all(Review).values():
                if v.id == self.place_id:
                    reviews_objs.append(v)
            return reviews_objs

        @property
        def amenities(self):
            """returns the list of Amenity instances
            of specific place
            """
            from models import storage
            from models.amenity import Amenity
            amenity_objs = []
            for v in storage.all(Amenity).values():
                if v.id in self.amenity_ids:
                    amenity_objs.append(v)
            return amenity_objs

        @amenities.setter
        def amenities(self, amenity):
            """add new aminity to place"""
            from models import storage
            from models.amenity import Amenity
            if type(amenity) is Amenity:
                self.amenity_ids.append(amenity.id)
