import os
import json
import requests
from datetime import datetime, timedelta

# API endpoint to fetch the URL of the Default Cards Bulk Data from Scryfall
api_url = "https://api.scryfall.com/bulk-data"

print("Fetching the URL of the Default Cards Bulk Data from Scryfall...")
# Fetch the bulk data types
response = requests.get(api_url)
bulk_data_types = response.json()["data"]

# Find the URL of the Default Cards Bulk Data
for data_type in bulk_data_types:
    if data_type["type"] == "default_cards":
        url = data_type["download_uri"]
        break

print(f"URL fetched: {url}")

# Path to the cached data
cache_path = "scryfall-default-cards.json"

# Check if the data is already cached
if os.path.exists(cache_path):
    # Get the timestamp of the cached data
    timestamp = os.path.getmtime(cache_path)
    cached_time = datetime.fromtimestamp(timestamp)
    # Check if the cached data is older than 24 hours
    if datetime.now() - cached_time > timedelta(hours=24):
        print("Cached data is older than 24 hours. Downloading updates...")
        # Download the data
        response = requests.get(url)
        data = response.json()
        # Cache the data
        with open(cache_path, "w") as f:
            json.dump(data, f)
        print("Data downloaded and cached.")
    else:
        print("Cached data is up to date. Loading data from cache...")
        # Load the cached data
        with open(cache_path, "r") as f:
            data = json.load(f)
else:
    print("Data not found in cache. Downloading...")
    # Download the data
    response = requests.get(url)
    data = response.json()
    # Cache the data
    with open(cache_path, "w") as f:
        json.dump(data, f)
    print("Data downloaded and cached.")

# Ask for the user's birth month and day
while True:
    try:
        birth_month = int(input("Enter your birth month (1-12): "))
        if 1 <= birth_month <= 12:
            break
        print("Invalid input. Please enter a number between 1 and 12.")
    except ValueError:
        print("Invalid input. Please enter a number.")

while True:
    try:
        birth_day = int(input("Enter your birth day (1-31): "))
        if 1 <= birth_day <= 31:
            break
        print("Invalid input. Please enter a number between 1 and 31.")
    except ValueError:
        print("Invalid input. Please enter a number.")

print("Filtering data...")
# Filter the data
filtered_data = []
for card in data:
    # Check if the card has the required promo types
    if "promo_types" in card and "datestamped" in card["promo_types"] and "prerelease" in card["promo_types"]:
        # Parse the release date
        release_date = datetime.strptime(card["released_at"], "%Y-%m-%d")
        # Check if the release date is before 2021-04-23
        if release_date < datetime(2021, 4, 23):
            # Check if the release date is within 10 days of the user's birth month and day
            birth_date = datetime(release_date.year, birth_month, birth_day)
            if abs((release_date - birth_date).days) <= 10:
                filtered_data.append(card)

# Sort the filtered data by how close the release date (ignoring the year) is to the user's birth date
filtered_data.sort(key=lambda card: abs((datetime(datetime.now().year, birth_month, birth_day) - (datetime(datetime.now().year, datetime.strptime(card["released_at"], "%Y-%m-%d").month, datetime.strptime(card["released_at"], "%Y-%m-%d").day) - timedelta(days=7))).days))

print(f"Found {len(filtered_data)} matching cards.")

print("Writing output to HTML file...")
# Output the images of the filtered cards to an HTML file
with open("output.html", "w") as f:
    f.write("<html>\n<body style='background-color: #333333;'>\n")
    if filtered_data:
        f.write("<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));'>\n")
        for card in filtered_data:
            # Check if the card has an image
            image_uri = None
            if "image_uris" in card and "border_crop" in card["image_uris"]:
                image_uri = card["image_uris"]["border_crop"]
            elif "card_faces" in card and "image_uris" in card["card_faces"][0] and "border_crop" in card["card_faces"][0]["image_uris"]:
                image_uri = card["card_faces"][0]["image_uris"]["border_crop"]

            if image_uri:
                f.write(f"<div style='border: 1px solid #000; margin: 10px; padding: 10px;'>\n")
                f.write(f"<a href='{card['scryfall_uri']}' target='_blank'>\n")
                f.write(f"<img src='{image_uri}' alt='{card['name']}' style='width: 100%;'>\n")
                f.write(f"</a>\n")
                f.write(f"</div>\n")
        f.write("</div>\n")
    else:
        f.write("<h1 style='color: white;'>Womp womp! There aren't any prerelease promos with your birthday on them. :(</h1>\n")
    f.write("</body>\n</html>")
print("Output written to output.html.")
