from server.repository.review_repository import ReviewRepository
from server.service.exceptions import ReviewNotFoundError


class ReviewService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self.review_repository = review_repository

    def get_review(self, review_id):
        review = self.review_repository.get(review_id)
        if review is None:
            raise ReviewNotFoundError()
        return review

    def create_review(self, restaurant_id, review_text, user_id, date):
        review = self.review_repository.add(restaurant_id, review_text, user_id, date)
        return review

    def list_review(self, restaurant_id):
        reviews = self.review_repository.list_for_restaurant(restaurant_id)
        return reviews

    def list_user_review(self, user_id):
        reviews = self.review_repository.list_for_user(user_id)
        return reviews

    def delete_review(self, review_id):
        review = self.review_repository.delete(review_id)
        return review


