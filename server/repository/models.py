import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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

    pass


class RestaurantModel(Base):
    pass
