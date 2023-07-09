import requests


class User:
    def __init__(self, id, name, email, dietary_preferences,
                 following_user_ids=set(), favorite_restaurant_ids=set()):
        self.id = id
        self.name = name
        self.email = email
        self.dietary_preferences = dietary_preferences

        # XXX: Is it okay to store them as IDs here? Maybe store as actual objects?
        self.following_user_ids = following_user_ids
        self.favorite_restaurant_ids = favorite_restaurant_ids

    # XXX: Do we need these?
    def follow_user(self, user_to_follow_id):
        self.following_user_ids.add(user_to_follow_id)

    def unfollow_user(self, user_to_unfollow_id):
        self.following_user_ids.remove(user_to_unfollow_id)

    def update_dietary_preferences(self, dietary_preferences):
        self.dietary_preferences = dietary_preferences
