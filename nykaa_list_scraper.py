import json
import time
import os
import csv
from curl_cffi import requests
from bs4 import BeautifulSoup

# Import existing ingredients scraper
try:
    from nykaa_ingredients_scraper import fetch_ingredients
except ImportError:
    # If import fails, we will define a dummy one or handle it
    def fetch_ingredients(url):
        return None

def fetch_category_products(page_url):
    """
    Fetches a single page of category listing and extracts product links.
    Returns: list of dicts with {'name', 'url'}
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    print(f"Fetching Category Page: {page_url}...")
    try:
        response = requests.get(page_url, headers=headers, impersonate="chrome120")
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        
        products_list = []
        for s in scripts:
            if s.string and '__PRELOADED_STATE__' in s.string:
                idx = s.string.find('=')
                if idx != -1:
                    json_str = s.string[idx+1:].strip()
                    if json_str.endswith(';'):
                        json_str = json_str[:-1]
                    
                    try:
                        data = json.loads(json_str)
                        c_listing = data.get('categoryListing', {})
                        list_data = c_listing.get('listingData', {})
                        products = list_data.get('products', [])
                        
                        for p in products:
                            name = p.get('name')
                            slug = p.get('slug')
                            if slug:
                                # Construct URL
                                url = f"https://www.nykaa.com/{slug}"
                                products_list.append({'name': name, 'url': url})
                                
                    except Exception as e:
                        print(f"JSON Parse Error: {e}")
                break
                
        return products_list

    except Exception as e:
        print(f"Request failed: {e}")
        return []

def scrape_category_and_ingredients(base_url, max_pages=1, delay=1, csv_filename="data/nykaa_ingredients_realtime.csv", category_name="Unknown"):
    """
    Scrapes product list and then fetches ingredients for EACH product.
    Saves results to CSV in real-time, including category name.
    """
    all_results = []
    
    # Ensure directory exists
    if os.path.dirname(csv_filename):
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        
    # Setup CSV Header if file doesn't exist
    write_header = not os.path.exists(csv_filename)
    fields = ['category', 'name', 'url', 'ingredients']
    
    # Check if header needs to be written even if file exists (maybe it's empty)
    if os.path.exists(csv_filename) and os.path.getsize(csv_filename) == 0:
        write_header = True

    for page in range(1, max_pages + 1):
        page_url = f"{base_url}?page_no={page}&sort=popularity"
        print(f"\n--- Scraping Page {page} ---")
        
        products = fetch_category_products(page_url)
        print(f"Found {len(products)} products on page {page}.")
        
        for i, p in enumerate(products):
            name = p['name']
            url = p['url']
            print(f"  [{i+1}/{len(products)}] Fetching ingredients for: {name}")
            
            ing_data = fetch_ingredients(url)
            
            ingredients = "Not Found"
            if ing_data and 'Ingredients' in ing_data:
                 ingredients = ing_data['Ingredients']
                 
            row = {
                'category': category_name,
                'name': name,
                'url': url,
                'ingredients': ingredients
            }
            all_results.append(row)
            
            # Save to CSV in Real-Time
            with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                if write_header:
                    writer.writeheader()
                    write_header = False  # Only write once
                # Clean ingredients string formatting for CSV safety
                clean_ing = ingredients.replace('\n', ' ').replace('\r', ' ')
                writer.writerow({
                    'category': category_name,
                    'name': name,
                    'url': url,
                    'ingredients': clean_ing
                })
                
            time.sleep(delay)
            
    return all_results

if __name__ == "__main__":
    # Test script standalone
    category_url = "https://www.nykaa.com/skin/moisturizers/face-moisturizer-day-cream/c/8394"
    print("Testing Nykaa List Scraper (1 page)...")
    results = scrape_category_and_ingredients(category_url, max_pages=1, delay=1)
    
    print(f"\nCollected {len(results)} items found with ingredients.")
    for idx, item in enumerate(results[:3]):  # Print first 3
        print(f"\n--- Item {idx+1} ---")
        print(f"Product: {item['name']}")
        print(f"Ingredients: {item['ingredients'][:100]}...")
