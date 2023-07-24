from sqlalchemy.orm import Session

from server.service.user import User
from server.repository.models import UserModel, RestaurantModel


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, name, email):
        new_user = UserModel(username=name, email=email)
        self.session.add(new_user)
        return new_user.dict()

    def _get_from_database(self, id):
        return self.session.query(UserModel).filter(
            UserModel.id == str(id)).first()

    def get(self, id):
        user = self._get_from_database(id)
        if user is not None:
            return user.dict()

    def delete(self, id):
        user = self._get_from_database(id)
        self.session.delete(user)
        return user

    def update(self, id, **payload):
        pass
