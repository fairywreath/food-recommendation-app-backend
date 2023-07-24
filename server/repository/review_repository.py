from sqlalchemy.orm import Session

from server.service.review import Review
from server.repository.models import UserModel, RestaurantModel, ReviewModel

class ReviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, restaurant_id, review_text, user_id, date):
        new_review = ReviewModel(restaurant_id, review_text, user_id, date)
        self.session.add(new_review)
        return new_review.dict()
    
    def _get_from_database(self,id):
        return self.session.query(ReviewModel).filter(
            ReviewModel.id == str(id)).first()
    
    def get(self, id):
        review = self._get_from_database(id)
        if review is not None:
            return Review(**review.dict())
    
    def delete(self, id):
        review = self._get_from_database(id)
        self.session.delete(review)
        return review.dict()
    
    def list_for_restaurant(self, id):
        query = self.session.query(ReviewModel)
        reviews = query.filter(ReviewModel.restaurant_id == str(id)).all()
        return [ReviewModel(**review.dict()) for review in reviews]

    def list_for_user(self, id):
        query = self.session.query(ReviewModel)
        reviews = query.filter(ReviewModel.user_id == str(id)).all()
        return [ReviewModel(**review.dict()) for review in reviews]
    