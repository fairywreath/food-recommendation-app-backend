from sqlalchemy.orm import Session

from server.repository.models import UserModel, RestaurantModel


class RestaurantsRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, restaurants):
        pass
    def get_from_database(self, id_):
        return self.session.query(UserModel).filter(
            UserModel.id == str(id)).first()

    def get(self, id_):
        return self.session.query(RestaurantModel).filter(RestaurantModel.id == str(id_)).first()


    def update(self, id_, **payload):
        restaurant = self.get(id_)

    def __delete__(self, id_):
        self.session.delete(self.get(id_))
    # XXX: Need update for reviews
    # def update(self, id, **payload):
    #     pass
