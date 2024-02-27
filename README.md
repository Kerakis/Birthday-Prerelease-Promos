# Birthday Prerelease Promos

This Python script fetches card data from the Scryfall API, filters the date-stamped prerelease promo cards based on the user's birth month and day, and generates an HTML file displaying the images of the filtered cards.

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository to your local machine.
2. Install the required Python library using `pip install requests`

## Usage

- Run the script using Python: `python birthday_prerelease.py`
- When prompted, enter your birth month (1-12) and birth day (1-31).
- The script will fetch the card data, filter the cards, and generate an HTML file named output.html.
- Open output.html in your web browser to view the images of the filtered cards.

## Notes

- The script caches the card data to avoid unnecessary API requests. The cached data is stored in a file named scryfall-default-cards.json.
- The script checks if the cached data is older than 24 hours and downloads updates if necessary.
- The script filters the cards based on the user's birth month and day. It includes a card in the filtered data if the card's release date is within 10 days of the user's birth date, regardless of the year. This is because the `release_date` for these cards is when the actual set released rather than what is stamped on the card. Manual verification is required.
- Prerelease promos created in Strixhaven and later are excluded, since these cards only include the year in their datestamp.
