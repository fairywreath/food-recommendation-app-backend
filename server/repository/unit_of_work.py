import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

DB_URL = os.getenv('DB_URL')
assert DB_URL is not None, 'DB_URL environment variable needed.'

# Or configure per config field
# password = os.environ["DB_PASS"]
# host = os.environ["DB_HOST"]
# port = os.environ["DB_PORT"]
# database = os.environ["DB_NAME"]
#
# DB_URL = f"mysql://{user}:{password}@{host}:{port}/{database}"

# XXX TODO: Use sqlaclhemy asynchronous IO


class UnitOfWork:
    def __init__(self):
        self.session_maker = sessionmaker(
            bind=create_engine(DB_URL)
        )

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
