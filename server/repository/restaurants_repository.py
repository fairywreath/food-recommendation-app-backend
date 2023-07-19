from sqlalchemy.orm import Session

from server.repository.models import UserModel, RestaurantModel


class RestaurantsRepository:
    def __init__(self, session: Session):
        self.session = session
