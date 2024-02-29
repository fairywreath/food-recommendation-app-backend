import pandas as pd
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer


DATA_FILE_PATH = "final_data.json"
COLLECTION_NAME = "restaurants_v4"


encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

# qdrant = QdrantClient(host="localhost", port=6333)

print("Connecting to qdrant client...")
qdrant = QdrantClient(
    url="https://6c83301a-82e1-44b4-b14e-60c6f04e2486.us-east-1-0.aws.cloud.qdrant.io:6333",
    api_key="DOcS9VYxs_5nqUi6ZgF0Ld6Psfk0kLNRbsZx8JKW4xoIABC2NOQ6Qg",
)
print("Successfully connected to Qdrant client")


# Creates a new collection, deletes an existing one with the same name.
# qdrant.recreate_collection(
#     collection_name=COLLECTION_NAME,
#     vectors_config=models.VectorParams(
#         size=encoder.get_sentence_embedding_dimension(),
#         distance=models.Distance.COSINE,
#     ),
#     shard_number=2,
# )


# Bulk upload entries.
# df = pd.read_json(DATA_FILE_PATH)
# # df = df.head(20)
# duplicates = df.duplicated(subset=["business_id"], keep=False)
# duplicated_rows = df[duplicates]
# assert duplicated_rows.empty
# data_dict = df.to_dict(orient='records')

# upload_res = qdrant.upload_records(
#     collection_name=COLLECTION_NAME,
#     records=[
#         models.Record(
#             id=idx, vector=encoder.encode(doc["text"]).tolist(), payload=doc
#         )
#         for idx, doc in enumerate(data_dict)
#     ],
# )

# collection_info = qdrant.get_collection(collection_name=COLLECTION_NAME)
# print(collection_info)


price_levels = ["$$"]
categories = ["japanese"]
minimum_rating = 4.0


def build_query_filters(categories, price_levels, minimum_rating, geoloc):
    musts = []

    if categories:
        musts.append(
            models.FieldCondition(
                key="categories",
                match=models.MatchAny(
                    any=categories),
            ),
        )

    if price_levels:
        musts.append(
            models.FieldCondition(
                key="price_level",
                match=models.MatchAny(
                    any=price_levels),
            ),
        )

    if minimum_rating:
        musts.append(
            models.FieldCondition(
                key="business_rating",
                range=models.Range(
                    gte=minimum_rating,
                ),
            )
        )

    if geoloc:
        musts.append(
            models.FieldCondition(
                key="location",
                geo_radius=models.GeoRadius(
                    center=models.GeoPoint(
                        lon=geoloc["lon"],
                        lat=geoloc["lat"],
                    ),
                    radius=geoloc["radius"],  # in meters
                ),
            )
        )

    if musts:
        return models.Filter(must=musts)
    else:
        return None


filter = build_query_filters(["Chinese"], ["$", "$$"], None, None)
print(filter)


#
# Neural search
#
search_query = "Chinese"
search_hits = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=encoder.encode(
        search_query).tolist(),
    query_filter=filter,
    limit=30,
)

# search_query = "korean"
# search_hits = qdrant.search(
#     collection_name=COLLECTION_NAME,
#     query_vector=encoder.encode(
#         search_query).tolist(),
#     query_filter=models.Filter(
#         must=[
#             # Cuisine genre filtering
#             models.Filter(
#                 should=[
#                     models.FieldCondition(
#                         key="categories",
#                         # match=models.MatchValue(value="Korean"),
#                         match=models.MatchAny(
#                             any=["Korean", "Japanese", "Chinese"]),
#                     ),
#                 ]),
#             # Price level filtering
#             models.Filter(
#                 should=[
#                     models.FieldCondition(
#                         key="price_level",
#                         # match=models.MatchValue(value="$$"),
#                         match=models.MatchAny(any=["$", "$$", "$$$", "$$$$"]),
#                     ),
#                 ]),
#             # Minimum rating?
#             models.Filter(
#                 must=[
#                     models.FieldCondition(
#                         key="business_rating",
#                         range=models.Range(
#                             gte=4.0,
#                         ),
#                     )
#                 ]
#             ),
#             # Geolocation?
#             models.FieldCondition(
#                 key="location",
#                 geo_radius=models.GeoRadius(
#                     center=models.GeoPoint(
#                         lon=-79.4107,
#                         lat=43.7617,
#                     ),
#                     radius=2000.0,  # in meters
#                 ),
#             )
#         ]
#     ),
#     limit=30,
# )


# search_hits = qdrant.search(
#     collection_name=COLLECTION_NAME,
#     query_vector=encoder.encode(
#         search_query).tolist(),
#     # query_filter=models.Filter(
#     #     must=[models.FieldCondition(key="year", range=models.Range(gte=2000))]
#     # ),
#     # limit=1,
#     limit=30,
# )

for hit in search_hits:
    payload = {key: value for key, value in hit.payload.items()
               if key != "text"}
    print(payload)


# Basic filtering
#
# filter_hits = qdrant.scroll(
#     collection_name=COLLECTION_NAME,
#     scroll_filter=models.Filter(
#         must=[
#             # models.FieldCondition(
#             #     key="rating",
#             #     match=models.MatchValue(value=4.5),
#             # ),
#             #     models.FieldCondition(
#             #         key="color",
#             #         match=models.MatchValue(value="red"),
#             #     ),
#             models.FieldCondition(
#                 key="name",
#                 match=models.MatchText(text="gyu-kaku"),
#             )
#         ]
#     ),
# )
# for hit in filter_hits:
#     print(hit)
