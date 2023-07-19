"""
Contains common business logic types and enums
"""

from enum import Enum

from pydantic import BaseModel, confloat


class CuisineGenre(Enum):
    THAI = 'Thai'
    VIETNAMESE = 'Vietnamese'
    SOUTHEAST_ASIAN = 'Southeast Asian'
    KOREAN = 'Korean'
    CHINESE = 'Chinese'
    JAPANESE = 'Japanese'
    INDIAN = 'Indian'
    ITALIAN = 'Italian'
    FRENCH = 'French'
    AMERICAN = 'American'
    MEXICAN = 'Mexican'
    SOUTH_AMERICAN = 'South American'
    MIDDLE_EASTERN = 'Middle Eastern'
    MEDITERRANEAN = 'Mediterranean'


class SpendingBudget(Enum):
    VERY_LOW = 'Very low'
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    VERY_HIGH = 'Very high'


class DietaryPreference(Enum):
    VEGAN = 'Vegan'
    VEGETARIAN = 'Vegetarian'
    PESCETARIAN = 'Pescetarian'
    GLUTEN_FREE = 'Gluten-Free'
    DAIRY_FREE = 'Dairy-Free'
    NUT_FREE = 'Nut-Free'
    HALAL = 'Halal'


class GeographicCoordinates(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)
