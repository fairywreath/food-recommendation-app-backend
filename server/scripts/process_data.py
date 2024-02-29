import pandas as pd
import json
import requests

ORIGINAL_DATASET = "combined_reviews.json"
DECORATED_DATASET = "restaurants_decorated_final.json"


def add_additional_columns_to_original_data():
    df = pd.read_json(ORIGINAL_DATASET)
    df['display_address'] = ''
    df['categories'] = ''
    df['price_level'] = ''
    df['business_rating'] = ''
    df['image_url'] = ''
    df.to_json(DECORATED_DATASET, orient='records', indent=4)


def count_undecorated_entries(df):
    empty_categories_count = (df['business_rating'] == '').sum()
    print("Number of entries where categories is empty:", empty_categories_count)


def decorate_from_other_dataset(other_dataset, df):
    other_df = pd.read_json(other_dataset)
    # other_df.set_index("id")
    print(len(other_df))

    for index, row in other_df.iterrows():
        bid = row["id"]

        matching_row = df[df["business_id"] == bid]
        matching_row_index = df.index[df["business_id"] == bid]

        if not matching_row.empty:
            matching_row_index = matching_row_index[0]

            df.loc[matching_row_index, "business_rating"] = row["rating"]
            df.loc[matching_row_index,
                   "display_address"] = ' '.join(row["location"]["display_address"])

            df.loc[matching_row_index, "image_url"] = row["image_url"]
            df.loc[matching_row_index, "price_level"] = row["price"]

            titles = [category["title"] for category in row["categories"]]
            titles = ','.join(titles)
            df.loc[matching_row_index, "categories"] = titles
        else:
            pass
            # print(f"No match found for id {bid}")


def get_business_details(api_key, business_id):
    url = f"https://api.yelp.com/v3/businesses/{business_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return (data, response.status_code)
    else:
        print(f"Failed to fetch details for business ID {business_id}")
        print(response.status_code)
        print(response.json())
        return (None, response.status_code)


df = pd.read_json(DECORATED_DATASET)
print(f"Total number of entries {len(df)}")
count_undecorated_entries(df)

# decorate_from_other_dataset("all_toronto_restaurants.json", df)
# decorate_from_other_dataset("all_toronto_restaurants_2.json", df)
# decorate_from_other_dataset("all_toronto_restaurants_5.json", df)

count_undecorated_entries(df)

# api_key = "css9Vf4WbqpNehcyHiRjR0BbVBEiNJqqY4I3Suu4cRWZxOEwFBYcKXM26u0MVk1MUCoQN2wL4wDsjTmQYiWQQbUC5uSzVLkjSrjhB7ARnL5W58emL976WAgMM965ZXYx"
# api_key = "MratzzTYWgOoqLGaapnq0efhNmNO0belhYmK1znSzHIdLgO7heRYeHTwkQYhJyVPgLEQDqcLhyjcS8QrpULX2LmKoLh58bgIRO_qDlQYThGXv3eLUG19RIhVDAe7ZXYx"

# for index, row in df.iterrows():
#     if pd.isna(row["categories"]) or not row["categories"]:
#         business_id = row["business_id"]
#         print(f"Fetching details for business ID {business_id}...")
#         details, sc = get_business_details(api_key, business_id)

#         if sc == 404 or sc == 403:
#             continue

#         if details:
#             display_address = " ".join(details.get(
#                 "location", {}).get("display_address", ""))
#             df.at[index, "display_address"] = display_address

#             df.at[index, "categories"] = ",".join(
#                 [category["title"] for category in details.get("categories", [])])
#             df.at[index, "price_level"] = details.get("price", "")
#             df.at[index, "business_rating"] = details.get("rating", "")
#             df.at[index, "image_url"] = details.get("image_url", "")
#         else:
#             break

#         # if curr == max_count:
#             # break
#         # curr += 1

# df.to_json("r2.json", orient="records", indent=4)

new_df = df[df['categories'] != ""]
new_df.to_json(DECORATED_DATASET, orient="records", indent=4)
