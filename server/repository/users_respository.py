from sqlalchemy.orm import Session

from server.service.users import User
from server.repository.models import UserModel, RestaurantModel


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user):
        record = UserModel(**user.dict())
        self.session.add(record)
        return record

    def _get_from_database(self, id):
        return self.session.query(UserModel).filter(
            UserModel.id == str(id)).first()

    def get(self, id):
        user = self._get_from_database(id)
        if user is not None:
            return User(**user.dict())

    def delete(self, id):
        self.session.delete(self.get_from_database(id))

    def update(self, id, **payload):
        pass
