import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class UserModel(Base):
    # XXX: Some options:
    #   1. Redeclare all models, better for scalability
    #   2. Use sqclacodegen for (1)
    #   3. Runtime reflection, `automap`
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True, default=generate_uuid())
    username = Column(String, nullable=False)
    email = Column(String)

    # cuisine_preferences = Column(JSON)
    # dietary_restrictions = Column(JSON)
    # favorite_restaurants = Column(JSON)
    # users_following = Column(JSON)
    # ratings = Column(JSON)
    # pictures = Column(BLOB)
    # search_history = Column(JSON, nullable=True)

    def dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.username,
            'email': self.email,
        }


class RestaurantModel(Base):
    __tablename__: 'restaurant'
    id = Column(String, primary_key=True, default=generate_uuid())
    name = Column(String)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
