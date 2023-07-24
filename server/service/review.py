
class Review:
    def __init__(self, id,restaurant_id, review_text, date, user_id=None) -> None:
        self.id = id
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.review_text = review_text
        self.date = date

    def get_review(self):
        return self.review_text
    
    def dict(self):
        return {
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'review_text': self.review_text,
            'date': self.date
        }