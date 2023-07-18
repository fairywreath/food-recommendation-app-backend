import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# XXX: Properly configure with AWS RDS
# DB_URL = os.getenv('DB_URL')

# assert DB_URL is not None, 'DB_URL environment variable needed.'

user = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
# database = os.environ["DB_NAME"]
#
DB_URL = f"mysql://{user}:{password}@{host}:{port}"


class UnitOfWork:
    def __init__(self):
        # XXX: Properly initialize the AWS RDS session
        self.session_maker = sessionmaker(
            bind=create_engine(DB_URL)
        )

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
