from sqlalchemy.orm import Session

from server.repository.models import UserModel, RestaurantModel
from server.service.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, name, address, longitude, latitude):
        new_restaurant = RestaurantModel(
            name=name, address=address, longitude=longitude, latitude=latitude)
        self.session.add(new_restaurant)
        return new_restaurant.dict()

    def _get_from_database(self, id):
        return self.session.query(RestaurantModel).filter(
            RestaurantModel.id == str(id)).first()

    def get(self, id):
        restaurant = self._get_from_database(id)
        if restaurant is not None:
            return restaurant.dict()

    def delete(self, id):
        restaurant = self._get_from_database(id)
        self.session.delete(restaurant)
        return restaurant

    def update(self, id, **payload):
        pass

    def list(self, limit=None, **filters):
        query = self.session.query(RestaurantModel)
        restaurants = query.filter_by(**filters).limit(limit=limit).all()
        return [RestaurantModel(**restaurant.dict()) for restaurant in restaurants]
