
class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

        # self.dietary_preferences = []

    def get_id(self):
        return self.id

    # This dict is used to create 'UserModel' objects that are added to the database, hence user id isnt revealed here
    def dict(self):
        return {
            'username': self.username,
            'email': self.email
        }
