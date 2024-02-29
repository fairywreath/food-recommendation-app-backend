"""
Business logic and integration with the machine learning model for the recommendation system here
"""
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import requests

COLLECTION_NAME = "restaurants_v4"


class RecommendedRestaurant:
    def __init__(self, name, address, rating, business_id, vector_id, categories, price_level, business_rating, image_url, lon, lat):
        self.name = name
        self.address = address
        self.rating = rating
        self.business_id = business_id
        self.vector_id = vector_id

        self.categories = categories
        self.price_level = price_level
        self.business_rating = business_rating
        self.image_url = image_url

        self.lon = lon
        self.lat = lat


class SearchFilters:
    def __init__(self, categories, price_levels, minimum_rating, geoloc):
        self.categories = categories
        self.price_levels = price_levels
        self.minimum_rating = minimum_rating
        self.geoloc = geoloc


def build_query_filters(filters):
    if filters is None:
        return None

    musts = []

    if filters.categories:
        musts.append(
            models.FieldCondition(
                key="categories",
                match=models.MatchAny(
                    any=filters.categories),
            ),
        )

    if filters.price_levels:
        musts.append(
            models.FieldCondition(
                key="price_level",
                match=models.MatchAny(
                    any=filters.price_levels),
            ),
        )

    if filters.minimum_rating:
        musts.append(
            models.FieldCondition(
                key="business_rating",
                range=models.Range(
                    gte=filters.minimum_rating,
                ),
            )
        )

    if filters.geoloc:
        musts.append(
            models.FieldCondition(
                key="location",
                geo_radius=models.GeoRadius(
                    center=models.GeoPoint(
                        lon=filters.geoloc.lon,
                        lat=filters.geoloc.lat,
                    ),
                    radius=filters.geoloc.radius,  # in meters
                ),
            )
        )

    if musts:
        return models.Filter(must=musts)
    else:
        return None


class RecommendationService:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.qdrant_client = QdrantClient(
            url="https://6c83301a-82e1-44b4-b14e-60c6f04e2486.us-east-1-0.aws.cloud.qdrant.io:6333",
            api_key="DOcS9VYxs_5nqUi6ZgF0Ld6Psfk0kLNRbsZx8JKW4xoIABC2NOQ6Qg",
        )

    def search(self, search_query, search_filters=None):
        print("Searching reccs in service...")

        filters = build_query_filters(search_filters)

        hits = self.qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=self.encoder.encode(
                search_query).tolist(),
            query_filter=filters,
            limit=50,
        )

        results = []
        for hit in hits:
            payload = hit.payload
            rr = RecommendedRestaurant(
                payload['name'], payload['postal_code'], payload['stars'], payload['business_id'], hit.id,
                payload["categories"], payload["price_level"], payload["business_rating"], payload["image_url"],
                payload["location"]["lon"], payload["location"]["lat"])
            if rr.address is None:
                # XXX: Hack if no postal code found :(. TODO: Just remove entries with no postal code
                rr.address = "N2L 3G9"
            results.append(rr)

        return results

    def recommend(self, positive_ids):
        hits = self.qdrant_client.recommend(
            collection_name=COLLECTION_NAME,
            positive=positive_ids,
            limit=15
        )

        # for hit in hits:
        #     results.append(get_yelp_business_details(
        #         API_KEY, hit.payload['business_id'], hit.id))
        results = []
        for hit in hits:
            payload = hit.payload
            rr = RecommendedRestaurant(
                payload['name'], payload['postal_code'], payload['stars'], payload['business_id'], hit.id,
                payload["categories"], payload["price_level"], payload["business_rating"], payload["image_url"],
                payload["location"]["lon"], payload["location"]["lat"])
            if rr.address is None:
                # XXX: Hack if no postal code found :(
                rr.address = "N2L 3G9"
            results.append(rr)

        return results
