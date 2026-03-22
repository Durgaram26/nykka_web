import csv
import time
import json
import os
from curl_cffi import requests

def fetch_reviews(product_id="22032", max_pages=60, delay=1):
    """
    Fetches reviews from the Nykaa API using curl_cffi to bypass anti-scraping.
    Uses sort=MOST_RECENT to get a mix of all ratings.
    """
    base_url = f"https://www.nykaa.com/gateway-api/products/{product_id}/reviews"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    all_reviews = []
    page = 1
    
    while page <= max_pages:
        # Added sort=MOST_RECENT to get all ratings chronologically
        url = f"{base_url}?pageNo={page}&sort=MOST_RECENT&domain=nykaa"
        print(f"Fetching Page {page}...")
        
        try:
            response = requests.get(url, headers=headers, impersonate="chrome120")
            
            if response.status_code != 200:
                print(f"Stop: Status code {response.status_code}")
                break
                
            data = response.json()
            review_data = data.get('response', {}).get('reviewData', [])
            
            if not review_data:
                print("No more reviews found. Stopping.")
                break
                
            print(f"Found {len(review_data)} reviews on page {page}.")
            
            for review in review_data:
                extracted_review = {
                    'User Name': review.get('name', 'N/A'),
                    'Rating': review.get('rating', 'N/A'),
                    'Date': review.get('createdOn', 'N/A'),
                    'Title': review.get('title', 'N/A'),
                    'Review Text': review.get('description', 'N/A'),
                    'Helpful Count': review.get('likeCount', 0),
                    'Label': review.get('label', 'N/A'),
                    'Skin Type': 'N/A',
                    'Skin Tone': 'N/A'
                }
                
                meta_data = review.get('metaData', {})
                if isinstance(meta_data, dict):
                    portfolio_form = meta_data.get('portfolioForm', [])
                    if isinstance(portfolio_form, list):
                        for item in portfolio_form:
                            display_text = item.get('displayText', '').lower()
                            attributes = item.get('attributes', [])
                            if attributes:
                                value = attributes[0].get('value', 'N/A')
                                if 'skin type' in display_text:
                                    extracted_review['Skin Type'] = value
                                elif 'skin tone' in display_text:
                                    extracted_review['Skin Tone'] = value

                all_reviews.append(extracted_review)
                
                # Stop early if we hit 1000 reviews
                if len(all_reviews) >= 1000:
                    print("Reached requested 1000 reviews limit. Stopping.")
                    return all_reviews

            page += 1
            time.sleep(delay)
            
        except Exception as e:
            print(f"An error occurred on page {page}: {e}")
            break
            
    return all_reviews

def save_to_csv(reviews, filename='nykaa_reviews_all.csv'):
    if not reviews:
        print("No reviews to save.")
        return
        
    fields = ['User Name', 'Rating', 'Date', 'Title', 'Review Text', 'Helpful Count', 'Label', 'Skin Type', 'Skin Tone']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for review in reviews:
            for k, v in review.items():
                if isinstance(v, str):
                     review[k] = v.replace('\n', ' ').replace('\r', ' ')
            writer.writerow(review)
            
    print(f"Successfully saved {len(reviews)} reviews to '{filename}'")

def main():
    print("Starting Nykaa Review Scraper (API-Based, sorting: MOST_RECENT)...")
    PRODUCT_ID = "22032" 
    
    # Run scraper
    reviews = fetch_reviews(PRODUCT_ID, max_pages=60, delay=1)
    
    print(f"\nTotal Reviews Collected: {len(reviews)}")
    if reviews:
        save_to_csv(reviews, 'nykaa_reviews_all_ratings.csv')
    else:
        print("No reviews collected loaded.")

if __name__ == "__main__":
    main()
