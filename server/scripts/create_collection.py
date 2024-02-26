import pandas as pd
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer


DATA_FILE_PATH = "combined_reviews.json"
COLLECTION_NAME = "restaurants_v2"


encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

# qdrant = QdrantClient(host="localhost", port=6333)

qdrant = QdrantClient(
    url="https://6c83301a-82e1-44b4-b14e-60c6f04e2486.us-east-1-0.aws.cloud.qdrant.io:6333",
    api_key="DOcS9VYxs_5nqUi6ZgF0Ld6Psfk0kLNRbsZx8JKW4xoIABC2NOQ6Qg",
)


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


#
# Neural search
#
search_query = "korean grill"
search_hits = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=encoder.encode(
        search_query).tolist(),
    limit=30,
)


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
