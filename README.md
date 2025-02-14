# Flipkart Reviews Scraper

This repository contains a Python script that scrapes product reviews from Flipkart using BeautifulSoup. It extracts essential review details such as review text, rating, review date, and verified buyer status, and then saves them into a CSV file for further analysis.

## Features

- **Review Scraping:** Extracts reviews from Flipkart product pages.
- **Pagination Handling:** Automatically detects and processes multiple review pages.
- **Data Extraction:** Retrieves key details like review text, rating, date, and buyer verification.
- **Sentiment Labeling:** Classifies reviews as _positive_, _neutral_, or _negative_ based on the rating.
- **CSV Export:** Consolidates the scraped data into a CSV file.
- **Robust Error Handling:** Manages connection errors and unexpected page structures gracefully.

## Technologies Used

- **Python 3.x**
- **Requests** – For handling HTTP requests.
- **BeautifulSoup (bs4)** – For parsing HTML content.
- **CSV Module** – For writing data to CSV.
- **Dateutil** – For date parsing and formatting.

## Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vn33/Flipkart-Reviews-Scraper-BeautifulSoup.git
   ```
2. **Install Dependencies:**
   Create a virtual environment (optional but recommended) and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure the Script:**
   - Open `scrape_reviews.py` and update the `product_links` list with the Flipkart product URLs you wish to scrape.
   - Optionally, modify the headers dictionary to suit your browsing environment.
4. **Run the Script:**
   ```bash
   python scrape_reviews.py
   ```
   The script will output the scraping progress and finally save all reviews in a file named `product_reviews.csv`.
## Disclaimer
This tool is intended for educational purposes only. Please ensure you comply with Flipkart's terms of service when using this script. The website structure may change over time, which can affect the script's functionality.
   
