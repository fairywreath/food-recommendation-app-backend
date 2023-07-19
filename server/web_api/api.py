import sys
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response
from server.repository.unit_of_work import UnitOfWork
from server.repository.restaurants_repository import RestaurantsRepository
from server.app import app

from server.repository.models import RestaurantModel, UserModel
from server.web_api.schemas import (
    GetUserRequestSchema, GetUserResponseSchema, UserItemSchema,
    GetRestaurantRequestSchema, GetRestaurantResponseSchema,
    GetRecommendationsFromPreferencesSchema, RecommendationsRequestSchema,
    DietaryPreferencesSchema, GetRecommendationsResponseSchema,
    RateRestaurantSchema, GetMultipleRestaurantsRequestSchema,
    GetMultipleRestaurantsResponseSchema)


@app.get("/")
async def test():
    with UnitOfWork() as unit_of_work:
        pass
    #     print("Testing inside unit of work!")
    #     new_car = CarModel(name="Ferrari12")
    #     unit_of_work.session.add(new_car)
    #     unit_of_work.commit()
    return {"message": "Hello World"}


@app.get("/users/{user_id}/space", response_model=GetUserResponseSchema)
def get_user_details(user_id: UUID):
    # with UnitOfWork() as unit_of_work:
    #     repo = RestaurantsRepository(unit_of_work.session)
    #     user = repo.get(user_id)
    # return {"user": user}
    pass


@app.post("/users/create", status_code=status.HTTP_201_CREATED,
          response_model=GetUserResponseSchema)
def create_user(user: UserItemSchema):
    pass


@app.put("/users/{user_id}/follow/{user_id_to_follow}")
def follow_user(user_id: UUID, user_id_to_follow: UUID):
    pass


@app.put("/users/{user_id}/unfollow/{user_id_to_follow}")
def unfollow_user(user_id: UUID, user_id_to_follow: UUID):
    pass


@app.put("/users/{user_id}/rate/{restaurant_id}")
def rate_restaurant(user_id: UUID, restaurant_id: UUID,
                    rating: RateRestaurantSchema):
    pass


# XXX: This is handled client-side, do we need this at all?
# def get_user_location...

@app.delete("/users/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response)
def delete_user(user_id: UUID):
    pass


@app.put("/users/{user_id}/modify_dietary")
def modify_user_dietary_preferences(
        user_id: UUID, dietary_preferences: DietaryPreferencesSchema):
    pass


@app.get("/restaurants/{restaurant_id}/details",
         response_model=GetRestaurantResponseSchema)
def get_restaurant_details(restaurant_id: UUID):
    pass


# XXX: This is not strictly required, but is nice
@app.get("/restaurants/multiple_details",
         response_model=GetMultipleRestaurantsResponseSchema)
def get_multiple_restaurant_details(
        restaurant_ids: GetMultipleRestaurantsRequestSchema):
    pass


@app.get("/recommendations", response_model=GetRecommendationsResponseSchema)
def get_recommendations(preferences: GetRecommendationsFromPreferencesSchema):
    pass


@app.get("/recommendations/{user_id}",
         response_model=GetRecommendationsResponseSchema)
def get_recommendations_from_user(
        user_id: UUID, recommendation_list_details: RecommendationsRequestSchema):
    pass


def receive_signal(signalNumber, frame):
    print('Received:', signalNumber)
    sys.exit()


@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)
