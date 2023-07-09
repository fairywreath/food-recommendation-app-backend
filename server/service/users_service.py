from server.service.exceptions import UserNotFoundError, APIIntegrationError, InvalidActionError
from server.repository.users_respository import UsersRepository


class UsersService:
    def __init(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def get_user(self, user_id):
        user = self.users_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f'User with id {user_id} not found')
        return user

    def create_user(self, item):
        return self.users_repository.add(item)

    def delete_user(self, user_id):
        user = self.users_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f'User with id {user_id} not found')
        return self.users_repository.delete(user_id)

    def follow_user(self, user_id, user_to_follow_user_id):
        # return self.users_repository.update
        pass

    def unfollow_user(self, user_id, user_to_unfollow_user_id):
        # return self.users_repository.update
        pass

    def update_dietary_preferences(self, user_id, dietary_preferences):
        # return self.users_repository.update
        pass

    def rate_restaurant(self, user_id, restaurant_id, rating):
        # return self.users_repository.update
        pass
