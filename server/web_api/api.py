import sys
import uuid
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException, Query
from starlette import status
from starlette.responses import Response
from starlette.requests import Request
from server.repository.unit_of_work import UnitOfWork
from server.repository.user_respository import UserRepository
from server.repository.restaurant_repository import RestaurantRepository
from server.repository.review_repository import ReviewRepository
from server.service.user_service import UserService
from server.service.restaurant_service import RestaurantService
from server.service.review_service import ReviewService
from server.service.user import User
from server.service.exceptions import UserNotFoundError
from server.service.exceptions import ReviewNotFoundError
from server.app import app

from server.service.recommendation_service import (
    RecommendationService, RecommendedRestaurant, SearchFilters)

from server.repository.models import RestaurantModel, UserModel
from server.web_api.schemas import (
    RestaurantSchema, GetUserResponseSchema, UserSchema,
    GetRestaurantRequestSchema, GetRestaurantResponseSchema,
    GetRecommendationsFromPreferencesSchema, RecommendationsRequestSchema,
    DietaryPreferencesSchema, GetRecommendationsResponseSchema,
    RateRestaurantSchema, GetMultipleRestaurantsRequestSchema,
    GetMultipleRestaurantsResponseSchema, DeleteUserResponseSchema,
    CreateUserResponseSchema, ReviewSchema,
    RecommendationSearchRequestSchema, RecommendationSearchResponseSchema,
    RecommendationSimilarityRequestSchema
)


reccomendation_service = RecommendationService()


@app.get("/")
async def test():
    with UnitOfWork() as unit_of_work:
        pass

        # Test create user
        # repo = UsersRepository(unit_of_work.session)
        # service = UsersService(repo)

        # Create dummb User
        # dummy_user = User(None, "testuser", "testemail2@yahoo.co.id")
        # created_user = service.create_user(dummy_user)
        # print(created_user.get_id())
        # unit_of_work.commit()

        # return created_user

    return {"message": "Hello World"}


@app.get("/users/{user_id}")
async def get_user_details(user_id: str):
    try:
        with UnitOfWork() as unit_of_work:
            repo = UserRepository(unit_of_work.session)
            user_service = UserService(repo)
            user = user_service.get_user(user_id=user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"user with ID {user_id} not found"
        )


@app.post("/users/create", status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserSchema):
    print("Detected create user POST request")
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        user_name = payload.name
        user_email = payload.email
        user = user_service.create_user(user_name, user_email)
        unit_of_work.commit()
        # return_payload = user

        # XXX: Correctly get generated ID here
    return user


@app.put("/users/{user_id}/follow/{user_id_to_follow}")
async def follow_user(user_id: UUID, user_id_to_follow: UUID):
    pass


@app.put("/users/{user_id}/unfollow/{user_id_to_follow}")
def unfollow_user(user_id: UUID, user_id_to_follow: UUID):
    pass


@app.put("/users/{user_id}/rate/{restaurant_id}")
async def rate_restaurant(user_id: UUID, restaurant_id: UUID,
                          rating: RateRestaurantSchema):
    pass


# XXX: This is handled client-side, do we need this at all?
# def get_user_location...

@app.delete("/users/delete")
async def delete_user(user_id: UUID = Query(..., description="The UUID of the user to delete")):
    try:
        with UnitOfWork() as unit_of_work:
            repo = UserRepository(unit_of_work.session)
            user_service = UserService(repo)
            delete_user = user_service.delete_user(user_id=user_id)
            unit_of_work.commit()
        return delete_user
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found"
        )


@app.put("/users/{user_id}/modify_dietary")
def modify_user_dietary_preferences(
        user_id: UUID, dietary_preferences: DietaryPreferencesSchema):
    pass


@app.post("/restaurants/create", status_code=status.HTTP_201_CREATED)
async def create_restaurant(payload: RestaurantSchema):
    with UnitOfWork() as unit_of_work:
        repo = RestaurantRepository(unit_of_work.session)
        restaurant_service = RestaurantService(repo)
        name = payload.name
        address = payload.address
        longitude = payload.longitude
        latitude = payload.latitude
        restaurant = restaurant_service.create_restaurant(
            name=name, address=address, longitude=longitude, latitude=latitude)
        unit_of_work.commit()
    return restaurant


@app.get("/restaurants/{restaurant_id}/details",
         response_model=GetRestaurantResponseSchema)
async def get_restaurant_details(restaurant_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = RestaurantRepository(unit_of_work.session)
            restaurant_service = RestaurantService(repo)
            restaurant = restaurant_service.get_restaurant(
                restaurant_id=restaurant_id)
        return restaurant
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant with ID {restaurant_id} not found")


# XXX: This is not strictly required, but is nice
@app.get("/restaurants/multiple_details",
         response_model=GetMultipleRestaurantsResponseSchema)
def get_multiple_restaurant_details(
        restaurant_ids: List[uuid.UUID]):
    # try:
    #     with UnitOfWork() as unit_of_work:
    #         repo = RestaurantRepository(unit_of_work.session)
    #         restaurant_service = RestaurantService(repo)
    #         restaurant_list = [restaurant_service.get_restaurant(restaurant_id=restaurant_id) for restaurant_id in restaurant_ids]
    #     return restaurant_list.dict()
    # except UserNotFoundError:
    #     raise HTTPException(
    #         status_code=404, detail=f"restaurants with ID {restaurant_ids} not found"
    #     )
    pass


@app.get("/restaurants/all")
async def get_all_restaurants(request: Request, limit: Optional[int] = None):
    try:
        with UnitOfWork() as unit_of_work:
            repo = RestaurantRepository(unit_of_work.session)
            restaurant_service = RestaurantService(repo)
            restaurant_list = restaurant_service.list_restaurants()
        return {"restaurants": [restaurant.dict() for restaurant in restaurant_list]}
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"restaurants with ID not found"
        )


@app.get("/recommendations", response_model=GetRecommendationsResponseSchema)
def get_recommendations(preferences: GetRecommendationsFromPreferencesSchema):
    pass


@app.get("/recommendations/{user_id}",
         response_model=GetRecommendationsResponseSchema)
def get_recommendations_from_user(
        user_id: UUID, recommendation_list_details: RecommendationsRequestSchema):
    pass


@app.get("/reviews/restaurant/{restaurant_id}")
async def get_reviews_for_restaurants(restaurant_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = ReviewRepository(unit_of_work.session)
            review_service = ReviewService(repo)
            review_list = review_service.list_review(restaurant_id)
        return {'reviews': [review.dict() for review in review_list]}
    except ReviewNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"no reviews for restaurant{restaurant_id}"
        )


@app.get("/reviews/user/{user_id}")
async def get_reviews_for_user(user_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = ReviewRepository(unit_of_work.session)
            review_service = ReviewService(repo)
            review_list = review_service.list_user_review(user_id)
        return {'reviews': [review.dict() for review in review_list]}
    except ReviewNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"no reviews for restaurant{user_id}"
        )


@app.delete("/reviews/delete/{review_id}")
async def delete_review(review_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = ReviewRepository(unit_of_work.session)
            review_service = ReviewService(repo)
            delete_review = review_service.delete_review(review_id=review_id)
            unit_of_work.commit()
        return delete_review
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"User with ID {review_id} not found"
        )


@app.post("/reviews/create", status_code=status.HTTP_201_CREATED)
async def add_reviews(payload: ReviewSchema):
    with UnitOfWork() as unit_of_work:
        repo = ReviewRepository(unit_of_work.session)
        review_service = ReviewService(repo)
        restaurant_id = payload.restaurant_id
        user_id = payload.user_id
        review_text = payload.review_text
        date = payload.date
        review = review_service.create_review(
            restaurant_id, review_text, user_id, date)
        unit_of_work.commit()
    return review


def recommended_restaurant_to_schema(rec):
    return RecommendationSearchResponseSchema(
        name=rec.name,
        address=rec.address,
        # rating=rec.rating,
        business_id=rec.business_id,
        vector_id=rec.vector_id,
        categories=rec.categories,
        price_level=rec.price_level,
        business_rating=rec.business_rating,
        image_url=rec.image_url,
        lon=rec.lon,
        lat=rec.lat
    )


@app.post("/search", status_code=status.HTTP_200_OK)
async def recommendations_search(payload: RecommendationSearchRequestSchema):
    search_filters = SearchFilters(
        payload.categories, payload.price_levels, payload.minimum_rating, payload.geo_radius)
    recommendations = reccomendation_service.search(
        payload.search_query, search_filters)

    results = []
    for rec in recommendations:
        results.append(recommended_restaurant_to_schema(rec))

    return results


@app.post("/search/similarity", status_code=status.HTTP_200_OK)
async def recommendations_search_similarity(payload: RecommendationSimilarityRequestSchema):
    recommendations = reccomendation_service.recommend(
        payload.vector_ids)

    results = []
    for rec in recommendations:
        results.append(recommended_restaurant_to_schema(rec))
    return results


def receive_signal(signalNumber, frame):
    """

    @param signalNumber:
    @param frame:
    """
    print('Received:', signalNumber)
    sys.exit()


@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)
