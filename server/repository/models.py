import uuid
from datetime import datetime
from typing import Final


from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, JSON, BLOB, Enum, ARRAY,
    Table, Float, UniqueConstraint, Text, PrimaryKeyConstraint, Date, Double,
    Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from server.service.types import DietaryPreference, CuisineGenre, SpendingBudget

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


ID_LENGTH: Final[int] = 32

#
# Tables to represent relationships
#
users_following = Table(
    'users_following',
    Base.metadata,
    Column('follower_id', String(ID_LENGTH), ForeignKey('user.id')),
    Column('followed_id', String(ID_LENGTH), ForeignKey('user.id')),
)


favorite_restaurants = Table(
    'favorite_restaurants',
    Base.metadata,
    Column('user_id', String(ID_LENGTH), ForeignKey('user.id')),
    Column('restaurant_id', String(ID_LENGTH), ForeignKey('restaurant.id'))
)

# XXX: Should this be part of Review(yes :p)
user_restaurant_rating = Table(
    'user_restaurant_rating',
    Base.metadata,
    Column('user_id', String(ID_LENGTH), ForeignKey('user.id')),
    Column('restaurant_id', String(ID_LENGTH), ForeignKey('restaurant.id')),
    Column('rating', Float)
)

#
# Table to store column "arrays"
#
user_dietary_preferences = Table(
    'user_dietary_preferences', Base.metadata,
    Column(
        'user_id', String(ID_LENGTH),
        ForeignKey('user.id'), nullable=False),
    Column(
        'dietary_preference', Enum(DietaryPreference), nullable=False),
    UniqueConstraint('user_id', 'dietary_preference')
)

user_cuisine_genres = Table(
    'user_cuisine_genres', Base.metadata,
    Column(
        'user_id', String(ID_LENGTH),
        ForeignKey('user.id')),
    Column(
        'cuisine_genre', Enum(CuisineGenre)),
    UniqueConstraint('user_id', 'cuisine_genre')
)

user_spending_budgets = Table(
    'user_spending_budgets', Base.metadata,
    Column(
        'user_id', String(ID_LENGTH),
        ForeignKey('user.id')),
    Column(
        'spending_budget', Enum(SpendingBudget)),
    UniqueConstraint('user_id', 'spending_budget')
)

restaurant_dietary_preferences = Table(
    'restaurant_dietary_preferences', Base.metadata,
    Column(
        'restaurant_id', String(ID_LENGTH),
        ForeignKey('restaurant.id')),
    Column(
        'dietary_preference', Enum(DietaryPreference)),
    UniqueConstraint('restaurant_id', 'dietary_preference')
)

restaurant_cuisine_genres = Table(
    'restaurant_cuisine_genres', Base.metadata,
    Column(
        'restaurant_id', String(ID_LENGTH),
        ForeignKey('restaurant.id')),
    Column(
        'cuisine_genre', Enum(CuisineGenre)),
    UniqueConstraint('restaurant_id', 'cuisine_genre')
)


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(String(ID_LENGTH), primary_key=True, default=generate_uuid())
    username = Column(String(64), nullable=False, unique=True)
    email = Column(String(64), nullable=False, unique=True)

    following = relationship(
        'UserModel',
        secondary=users_following,
        primaryjoin=(users_following.c.follower_id == id),
        secondaryjoin=(users_following.c.followed_id == id),
        backref='followers'
    )

    favorite_restaurants = relationship(
        'RestaurantModel',
        secondary=favorite_restaurants,
        backref='favorited_by'
    )

    rated_restaurants = relationship(
        'RestaurantModel',
        secondary=user_restaurant_rating,
        backref='ratings',
        passive_deletes=True
    )

    reviewed_restaurants = relationship(
        'ReviewModel', back_populates="user")

    # XXX: Right now we have separate tables to list all dietary preferences etc. Is it better to store these as strings?

# pictures = Column(BLOB)
# search_history = Column(JSON, nullable=True)

# def dict(self):
#     return {
#         'user_id': self.user_id,
#         'user_name': self.username,
#         'email': self.email,
#     }


class RestaurantModel(Base):
    __tablename__ = 'restaurant'

    id = Column(String(ID_LENGTH), primary_key=True, default=generate_uuid())
    name = Column(String(64), nullable=False, unique=True)

    address = Column(String(64))
    website = Column(String(64))
    phone_number = Column(String(64))

    operating_hours = Column(String(64))
    by_reservation_only = Column(Boolean)

    latitude = Column(Float)
    longitude = Column(Float)

    spending_budget = Column(Enum(SpendingBudget))

    reviewers = relationship('ReviewModel', back_populates='restaurant')

    # average_rating = Column(Float)

    # def dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'address': self.address,
    #         'latitude': self.latitude,
    #         'longitude': self.longitude
    #     }


class ReviewModel(Base):
    __tablename__ = 'review'

    id = Column(String(ID_LENGTH), primary_key=True, default=generate_uuid())
    user_id = Column(String(ID_LENGTH), ForeignKey('user.id'))
    restaurant_id = Column(String(ID_LENGTH), ForeignKey('restaurant.id'))
    review_text = Column(Text)
    # rating = Column(Integer)
    date = Column(Date)

    user = relationship('UserModel', back_populates='reviewed_restaurants')
    restaurant = relationship('RestaurantModel', back_populates='reviewers')

    __table_args__ = (
        UniqueConstraint('user_id', 'restaurant_id'),
    )
