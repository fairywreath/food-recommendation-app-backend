from sqlalchemy.orm import Session

from server.repository.models import UserModel, RestaurantModel


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, item):
        self.session.add(item)

    def get_from_database(self, id):
        return self.session.query(UserModel).filter(
            UserModel.id == str(id)).first()

    def get(self, id):
        pass

    def update(self, id, **payload):
        pass

    def delete(self, id):
        self.session.delete(self.get_from_database(id))
