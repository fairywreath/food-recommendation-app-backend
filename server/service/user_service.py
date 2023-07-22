from server.service.exceptions import UserNotFoundError, APIIntegrationError, InvalidActionError
from server.repository.user_respository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id):
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f'User with id {user_id} not found')
        return user

    def create_user(self, name, email):
        return self.user_repository.add(name, email)

    def delete_user(self, user_id):
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f'User with id {user_id} not found')
        return self.user_repository.delete(user_id)

    def follow_user(self, user_id, user_to_follow_user_id):
        pass

    def unfollow_user(self, user_id, user_to_unfollow_user_id):
        pass

    def update_dietary_preferences(self, user_id, dietary_preferences):
        pass

    def rate_restaurant(self, user_id, restaurant_id, rating):
        pass
