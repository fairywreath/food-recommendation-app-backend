from sqlalchemy.orm import Session

from server.repository.models import UserModel, RestaurantModel


class RestaurantsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_from_database(self, id):
        return self.session.query(UserModel).filter(
            UserModel.id == str(id)).first()

    def get(self, id):
        pass

    # XXX: Need update for reviews
    # def update(self, id, **payload):
    #     pass
