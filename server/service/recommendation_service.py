"""
Business logic and integration with the machine learning model for the recommendation system here
"""
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import requests


class RecommendedRestaurant:
    def __init__(self, name, address, rating):
        self.name = name
        self.address = address
        self.rating = rating


def get_yelp_business_details(api_key, business_id):
    # Yelp API endpoint for business details
    api_url = f'https://api.yelp.com/v3/businesses/{business_id}'

    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    print(f"Yelp API request business details id {business_id}")
    # Make the API request
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        business_data = response.json()

        name = business_data['name']
        address = business_data['location']['display_address']
        rating = business_data.get('rating', 'N/A')

        return RecommendedRestaurant(name, ' '.join(address), rating)
    else:
        print(
            f"Error: Unable to fetch business details. Status code: {response.status_code}")
        print(response.text)

        return RecommendedRestaurant('dummy', ' '.join(["dummy", "address"]), 0.7)


API_KEY = "css9Vf4WbqpNehcyHiRjR0BbVBEiNJqqY4I3Suu4cRWZxOEwFBYcKXM26u0MVk1MUCoQN2wL4wDsjTmQYiWQQbUC5uSzVLkjSrjhB7ARnL5W58emL976WAgMM965ZXYx"


class RecommendationService:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.qdrant_client = QdrantClient(host="localhost", port=6333)

    def search(self, search_query):
        print("Searching reccs in service...")

        hits = self.qdrant_client.search(
            collection_name="my_restaurants",
            query_vector=self.encoder.encode(
                search_query).tolist(),
            limit=30,
        )

        results = []
        for hit in hits:
            results.append(get_yelp_business_details(
                API_KEY, hit.payload['business_id']))

        return results

    def recommend(self, positive_ids):
        hits = self.qdrant_client.recommend(
            collection_name="my_restaurants",
            positive=positive_ids,
            limit=20
        )

        results = []
        for hit in hits:
            results.append(get_yelp_business_details(
                API_KEY, hit.payload['business_id']))

        return results
