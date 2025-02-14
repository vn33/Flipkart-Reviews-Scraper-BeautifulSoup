import requests
from bs4 import BeautifulSoup
import csv
import time
from dateutil import parser as dateparser
import re

def get_soup(url, headers):
    """Download webpage and return BeautifulSoup object with error handling"""
    print(f"Downloading: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def extract_product_info(product_url):
    """Extract product slug and ID from Flipkart product URL"""
    try:
        if "/p/" not in product_url:
            return None, None
            
        base_part, product_part = product_url.split("/p/", 1)
        product_slug = base_part.split("/")[-1]
        product_id = product_part.split("?")[0].split("/")[0]
        return product_slug, product_id
    except Exception as e:
        print(f"URL parsing error: {str(e)}")
        return None, None

def extract_reviews(soup):
    """Extract reviews from a review page soup"""
    reviews = []
    for block in soup.find_all('div', class_='EKFha-'):
        try:
            review_text = block.select_one('.ZmyHeo').get_text(strip=True).replace('READ MORE', '') or ''
            rating = ''.join(filter(str.isdigit, block.select_one('.XQDdHH').get_text())) or '0'
            rating = float(rating)
            date_tags = block.select('._2NsDsF')
            date_str = date_tags[1].get_text(strip=True) if len(date_tags) > 1 else ''
            label = "positive" if rating > 4 else ("negative" if rating < 4 else "neutral") 
            
            # try:
            #     review_date = dateparser.parse(date_str).strftime('%d %b %Y') if date_str else ''
            # except:
            review_date = date_str
                
            verified = 'Yes' if 'Certified Buyer' in block.get_text() else 'No'
            
            reviews.append({
                "Review Text": review_text,
                "Review Rating": rating,
                "Review Date": review_date,
                "Reviewer Verified": verified,
                "Label": label
            })
        except Exception as e:
            print(f"Error parsing review block: {str(e)}")
    return reviews



def get_total_pages(soup):
    """Calculate total pages from review count."""
    # Locate the pagination div
    pagination_div = soup.find('div', class_='F2+K4v')

    if not pagination_div:
        return 1  # Default to 1 page if no pagination div is found

    # Extract all span elements
    spans = pagination_div.find_all('span')

    # Check if spans exist
    if not spans:
        return 1  # Default to 1 page if no spans are found

    try:
        # Extract text from all spans
        pagination_texts = [span.get_text(strip=True) for span in spans]

        # Join texts for processing (if necessary)
        combined_text = " ".join(pagination_texts)
        print(combined_text)

        # Extract the total reviews count using regex
        total_reviews = int(re.split(r'and|&', combined_text)[-1].split()[0])
        print('total reviews count', total_reviews)
        # Calculate total pages (10 reviews per page)
        return (total_reviews + 9) // 10
    except (ValueError, IndexError):
        # Handle errors related to text parsing or conversions
        return 1


def scrape_product_reviews(product_link, headers):
    """Main scraping function for a single product"""
    product_slug, product_id = extract_product_info(product_link)
    if not product_slug or not product_id:
        return []

    product_name = product_slug.replace("-", " ").title()
    reviews_url = f"https://www.flipkart.com/{product_slug}/product-reviews/{product_id}?page=1"
    
    first_page_soup = get_soup(reviews_url, headers)
    if not first_page_soup:
        return []

    total_pages = get_total_pages(first_page_soup)
    print(f"{product_name}, total pages: {total_pages}")
    all_reviews = []

    for page in range(1, total_pages + 1):
        page_url = f"https://www.flipkart.com/{product_slug}/product-reviews/{product_id}?page={page}"
        page_soup = get_soup(page_url, headers)
        
        if page_soup:
            page_reviews = extract_reviews(page_soup)
            for review in page_reviews:
                review.update({
                    "Product Name": product_name,
                    "Product ID": product_id
                })
            all_reviews.extend(page_reviews)
            
        time.sleep(1.5)  # Rate limiting protection

    return all_reviews

def main():
    headers = {
        "User-Agent": "..add your browser user agent..", # go to browser console by inspecting, and type "navigator.userAgent", it will provde you the user agent
        "Accept-Language": "en-US,en;q=0.9"
    }

    # Add multiple product links here
    product_links = [
        "https://www.flipkart.com/nike-tanjun-sneakers-men/p/itm8e91ca2199e63",
        "https://www.flipkart.com/blue-star-2024-model-0-8-ton-3-split-inverter-ac-white/p/itm0addbca1ef446",
        "https://www.flipkart.com/glx-1008-10-w-bluetooth-tower-speaker/p/itm3cfdfb1649501"
    ]

    all_reviews = []
    for link in product_links:
        print(f"\nScraping product: {link}")
        product_reviews = scrape_product_reviews(link, headers)
        all_reviews.extend(product_reviews)
        print(f"Found {len(product_reviews)} reviews")

    # Save all reviews to CSV
    with open("product_reviews.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Product Name", "Product ID", "Review Text", 
            "Review Rating", "Review Date", "Reviewer Verified", "Label"
        ], quoting=csv.QUOTE_ALL)
        
        writer.writeheader()
        writer.writerows(all_reviews)

    print(f"\nSuccessfully saved {len(all_reviews)} reviews to product_reviews.csv")

if __name__ == "__main__":
    main()