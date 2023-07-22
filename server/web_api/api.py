import sys
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from server.repository.unit_of_work import UnitOfWork
from server.repository.user_respository import UserRepository
from server.repository.restaurant_repository import RestaurantRepository

from server.service.user_service import UserService
from server.service.restaurant_service import RestaurantService
from server.service.user import User
from server.service.exceptions import UserNotFoundError
from server.app import app

from server.repository.models import RestaurantModel, UserModel
from server.web_api.schemas import (
    RestaurantSchema, GetUserResponseSchema, UserSchema,
    GetRestaurantRequestSchema, GetRestaurantResponseSchema,
    GetRecommendationsFromPreferencesSchema, RecommendationsRequestSchema,
    DietaryPreferencesSchema, GetRecommendationsResponseSchema,
    RateRestaurantSchema, GetMultipleRestaurantsRequestSchema,
    GetMultipleRestaurantsResponseSchema, DeleteUserResponseSchema, CreateUserResponseSchema)


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


@app.get("/users/{user_id}/space", response_model=GetUserResponseSchema)
async def get_user_details(user_id: str):
    try:
        with UnitOfWork as unit_of_work:
            repo = UserRepository(unit_of_work.session)
            user_service = UserService(repo)
            user = user_service.get_user(user_id=user_id)
        return user.dict()
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"user with ID {user_id} not found"
        )


@app.post("/users/create", status_code=status.HTTP_201_CREATED,
          response_model=CreateUserResponseSchema)
async def create_user(payload: UserSchema):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        user_name = payload.name
        user_email = payload.email
        user = user_service.create_user(user_name, user_email)
        unit_of_work.commit()
        # return_payload = user
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

@app.delete("/users/{user_id}/delete",
            response_model=DeleteUserResponseSchema)
async def delete_user(user_id: UUID):
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
        restaurant = restaurant_service.create_restaurant(name=name, address=address, longitude=longitude, latitude=latitude)
        unit_of_work.commit()
    return restaurant

@app.get("/restaurants/{restaurant_id}/details",
         response_model=GetRestaurantResponseSchema)
async def get_restaurant_details(restaurant_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = RestaurantRepository(unit_of_work.session)
            restaurant_service = RestaurantService(repo)
            restaurant = restaurant_service.get_restaurant(restaurant_id=restaurant_id)
        return restaurant.dict()
    except UserNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Restaurant with ID {restaurant_id} not found"
        )

# XXX: This is not strictly required, but is nice
@app.get("/restaurants/multiple_details",
         response_model=GetMultipleRestaurantsResponseSchema)
def get_multiple_restaurant_details(
        restaurant_ids: GetMultipleRestaurantsRequestSchema):
    # try:
    #     with UnitOfWork as unit_of_work:
    #         repo = RestaurantsRepository(unit_of_work.session)
    #         restaurant_service = RestaurantService(repo)
    #         user = restaurant_service.get_restaurant(restaurant_id=res)
    #     return user.dict()
    # except UserNotFoundError:
    #     raise HTTPException(
    #         status_code=404, detail=f"user with ID {restaurant_ids} not found"
    #     )
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
