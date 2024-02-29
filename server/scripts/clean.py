import json


# Read the JSON file
with open("data.json", "r") as file:
    data = json.load(file)

# Dictionary to keep track of seen business IDs
# seen_business_ids = set()

# Clean the data and ensure unique business IDs
# cleaned_data = []
# for entry in data:
# Replace incorrect "\/" characters with "/"
# entry["categories"] = entry["categories"].replace("\\/", "/")
# entry["image_url"] = entry["image_url"].replace("\\/", "/")
# Split the categories entry by "," to an array
# entry["categories"] = entry["categories"].split(",")

# Check if the business ID is unique
# if entry["business_id"] not in seen_business_ids:
#     cleaned_data.append(entry)
#     seen_business_ids.add(entry["business_id"])
# else:
#     print(
#         f"Duplicate business ID found: {entry['business_id']}. Skipping...")

# Write the cleaned data to a new JSON file
# with open("cleaned_data.json", "w") as file:
# json.dump(cleaned_data, file, indent=4)

# print("Cleaned data saved to 'cleaned_data.json'")


def get_unique_categories(data):
    unique_categories = set()

    # Extract unique categories from each entry
    for entry in data:
        categories = entry["categories"]
        unique_categories.update(categories)

    # Print the unique categories
    print("Unique categories:")
    for category in unique_categories:
        print(category)


for entry in data:
    # Assign "location" key with latitude and longitude
    # entry['location'] = {
    #     "lon": entry['longitude'],
    #     "lat": entry['latitude']
    # }
    # # Remove the original latitude and longitude
    # entry.pop('latitude', None)
    # entry.pop('longitude', None)

    # Append additional sentence to the start of text
    entry['text'] = f"The restaurant's name is {entry['name']}. {entry['text']}"

# Write the modified data back to the file
with open('final_data.json', 'w') as file:
    json.dump(data, file, indent=4)
