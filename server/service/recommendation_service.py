"""
Business logic and integration with the machine learning model for the recommendation system here
"""
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import requests


class RecommendedRestaurant:
    def __init__(self, name, address, rating, business_id, vector_id):
        self.name = name
        self.address = address
        self.rating = rating
        self.business_id = business_id
        self.vector_id = vector_id


def get_yelp_business_details(api_key, business_id, vector_id):
    # Yelp API endpoint for business details
    api_url = f'https://api.yelp.com/v3/businesses/{business_id}'

    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    print(
        f"Yelp API request business details id {business_id}, vector id {vector_id}")
    # Make the API request
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        business_data = response.json()

        name = business_data['name']
        address = business_data['location']['display_address']
        rating = business_data.get('rating', 'N/A')

        return RecommendedRestaurant(name, ' '.join(address), rating, business_id, vector_id)
    else:
        print(
            f"Error: Unable to fetch business details. Status code: {response.status_code}")
        print(response.text)

        return RecommendedRestaurant('dummy', ' '.join(["dummy", "address"]), 0.7, business_id, vector_id)


def get_business_details():
    pass


# API_KEY = "css9Vf4WbqpNehcyHiRjR0BbVBEiNJqqY4I3Suu4cRWZxOEwFBYcKXM26u0MVk1MUCoQN2wL4wDsjTmQYiWQQbUC5uSzVLkjSrjhB7ARnL5W58emL976WAgMM965ZXYx"
# API_KEY = "MratzzTYWgOoqLGaapngOethNmNOobelhYmK1znSzHIdLgO7heRYeHTWkQYhJyVPgLEQDgcLhyicS8QrpULX2LmKoLh58bgIRO_qDIQYThGXv3eLUG19RIhVDAe7ZXYx"
API_KEY = "MratzzTYWgOoqLGaapnq0efhNmNO0belhYmK1znSzHIdLgO7heRYeHTwkQYhJyVPgLEQDqcLhyjcS8QrpULX2LmKoLh58bgIRO_qDlQYThGXv3eLUG19RIhVDAe7ZXYx"


class RecommendationService:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.qdrant_client = QdrantClient(
            url="https://6c83301a-82e1-44b4-b14e-60c6f04e2486.us-east-1-0.aws.cloud.qdrant.io:6333",
            api_key="DOcS9VYxs_5nqUi6ZgF0Ld6Psfk0kLNRbsZx8JKW4xoIABC2NOQ6Qg",
        )

    def search(self, search_query):
        print("Searching reccs in service...")

        hits = self.qdrant_client.search(
            collection_name="restaurants_v1",
            query_vector=self.encoder.encode(
                search_query).tolist(),
            limit=15,
        )

        results = []
        for hit in hits:
            payload = hit.payload
            rr = RecommendedRestaurant(
                payload['name'], payload['postal_code'], payload['stars'], payload['business_id'], hit.id)
            if rr.address is None:
                # XXX: Hack if no postal code found :(
                rr.address = "N2L 3G9"
            results.append(rr)

        return results

    def recommend(self, positive_ids):
        hits = self.qdrant_client.recommend(
            collection_name="restaurants_v1",
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
                payload['name'], payload['postal_code'], payload['stars'], payload['business_id'], hit.id)
            if rr.address is None:
                # XXX: Hack if no postal code found :(
                rr.address = "N2L 3G9"
            results.append(rr)

        return results
