from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, conint, conlist, validator, constr

from server.service.types import CuisineGenre, SpendingBudget, DietaryPreference, GeographicCoordinates


# XXX: Clean this up, split into multiple files

class DietaryPreferencesSchema(BaseModel):
    genres: conlist(CuisineGenre)
    budget: Optional[SpendingBudget]
    dietary_preference: conlist(DietaryPreference)


class UserSchema(BaseModel):
    name: str
    email: str
    # dietary_preferences: DietaryPreferencesSchema = None
    # favorite_restaurant_ids: conlist(conint) = None
    # following_user_ids: conlist(conint) = None


class RestaurantSchema(BaseModel):
    name: str
    address: str
    longitude: str
    latitude: str


class ReviewSchema(BaseModel):
    user_id: str
    restaurant_id: str
    review_text: str
    date: str


class CreateUserRequestSchema(BaseModel):
    user: UserSchema

    class Config:
        extra = Extra.forbid


class CreateUserResponseSchema(BaseModel):
    id: UUID


class DeleteUserResponseSchema(BaseModel):
    id: UUID
    name: str
    email: str


class GetUserRequestSchema(BaseModel):
    id: UUID

    class Config:
        extra = Extra.forbid


class GetUserResponseSchema(BaseModel):
    user: UserSchema


class RestaurantItemSchema(BaseModel):
    cuisine_genre: CuisineGenre
    budget: SpendingBudget
    average_rating: conint
    address: constr
    website: constr
    geographic_coordinates: GeographicCoordinates

    # Extra restaurant description? Pictures?

    # XXX: Where should we put user text reviews?


# XXX: Have a robust review schema
# class RestaurantReview(BaseModel):
#     restaurant_id: UUID
#     text: constr(min_length=1)


class GetRestaurantRequestSchema(BaseModel):
    id: UUID

    class Config:
        extra = Extra.forbid


class GetRestaurantResponseSchema(BaseModel):
    name: str
    address: str
    longitude: float
    latitude: float

    class Config:
        extra: Extra.forbid


class GetMultipleRestaurantsRequestSchema(BaseModel):
    restaurant_ids: conlist(UUID, min_length=1)

    class Config:
        extra = Extra.forbid


class GetMultipleRestaurantsResponseSchema(BaseModel):
    restaurants: conlist(RestaurantItemSchema)


class RecommendationsRequestSchema(BaseModel):
    geographic_coordinates: GeographicCoordinates

    # XXX: Need extra location parameters? eg. maximum distance
    # location_parameters

    # XXX: Number of recommendations and paging
    amount: conint = 10
    # page: conint

    # similar_restaurants: conlist(UUID)


class GetRecommendationsFromPreferencesSchema(RecommendationsRequestSchema):
    dietary_preferences: DietaryPreferencesSchema

    class Config:
        extra = Extra.forbid


class GetRecommendationsResponseSchema(BaseModel):
    restaurant_ids: conlist(UUID)


class RateRestaurantSchema(BaseModel):
    rating: conint(ge=0, le=10)


class RecommendationSearchRequestSchema(BaseModel):
    search_query: str


class RecommendationSearchResponseSchema(BaseModel):
    name: str
    address: str
    rating: float

    # For testing/demo
    business_id: str    # YELP business id
    vector_id: int      # qdrant vector db id


class RecommendationSimilarityRequestSchema(BaseModel):
    vector_ids: conlist(int)
