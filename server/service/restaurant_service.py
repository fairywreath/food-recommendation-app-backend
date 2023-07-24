from server.repository.restaurant_repository import RestaurantRepository
from server.service.exceptions import RestaurantNotFoundError

class RestaurantService:
    def __init__(self, restaurant_repository: RestaurantRepository) -> None:
        self.restaurant_repository = restaurant_repository

    def get_restaurant(self, restaurant_id):
        restaurant = self.restaurant_repository.get(restaurant_id)
        if restaurant is None:
            raise RestaurantNotFoundError(f'Restaurant with id {restaurant_id} not found')
        return restaurant
    
    def list_restaurants(self, **filters):
        limit = filters.pop("limit", None)
        return self.restaurant_repository.list(limit=limit, **filters)
    
    def create_restaurant(self, name, address, longitude, latitude):
        return self.restaurant_repository.add(name=name, address=address, longitude=longitude, latitude=latitude)
    
    def delete_restaurnat(self, restaurant_id):
        restaurant = self.restaurant_repository.get(restaurant_id)
        if restaurant is None:
            raise RestaurantNotFoundError(f'Restaurant with id {restaurant_id} not found')
        return self.restaurant_repository.delete(restaurant_id)
    
    