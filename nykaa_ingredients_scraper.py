import json
import csv
import sys
import os
from bs4 import BeautifulSoup
from curl_cffi import requests

def fetch_ingredients(url):
    """
    Fetches ingredients from a Nykaa product page URL.
    Attempts to parse window.__PRELOADED_STATE__ inside script tags.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    print(f"Fetching Product Page: {url}...")
    try:
        response = requests.get(url, headers=headers, impersonate="chrome120")
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        
        # 1. Look inside __PRELOADED_STATE__
        for s in scripts:
            if s.string and '__PRELOADED_STATE__' in s.string:
                idx = s.string.find('=')
                if idx != -1:
                    json_str = s.string[idx+1:].strip()
                    if json_str.endswith(';'):
                        json_str = json_str[:-1]
                    
                    try:
                        data = json.loads(json_str)
                        
                        def find_key(obj, key):
                            if isinstance(obj, dict):
                                for k, v in obj.items():
                                    if k == key:
                                        return v
                                    item = find_key(v, key)
                                    if item is not None:
                                        return item
                            elif isinstance(obj, list):
                                for item in obj:
                                    result = find_key(item, key)
                                    if result is not None:
                                        return result
                            return None
                            
                        # Extract ingredients
                        ingredients_html = find_key(data, 'ingredients')
                        
                        # Also extract Product Name for context
                        product_name = 'N/A'
                        product_data = find_key(data, 'product')
                        if product_data and isinstance(product_data, dict):
                            product_name = product_data.get('name', 'N/A')
                        
                        if ingredients_html:
                            clean_ingredients = BeautifulSoup(ingredients_html, 'html.parser').get_text().strip()
                            return {
                                'Product Name': product_name,
                                'Ingredients': clean_ingredients,
                                'URL': url
                            }
                    except Exception as e:
                         print(f"Parse error: {e}")
                         
        # 2. Fallback: Search for static HTML elements with 'Ingredients' heading
        # Some pages might have it in description text directly in DOM
        headers_found = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for header in headers_found:
            if 'ingredients' in header.get_text().lower():
                # Get next sibling content
                sibling = header.find_next_sibling()
                if sibling:
                    return {
                        'Product Name': soup.title.get_text() if soup.title else 'N/A',
                        'Ingredients': sibling.get_text().strip(),
                        'URL': url
                    }

        print("Ingredients not found on this page layout.")
        return None

    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 nykaa_ingredients_scraper.py <URL>")
        # Default test URL for safety
        #test_url = "https://www.nykaa.com/cetaphil-cleansing-lotion/p/22032?skuId=22031"
        test_url="https://www.nykaa.com/nykaa-cosmetics-x-naagin-hot-sauce-plumping-lip-gloss/p/22062112?productId=22062112&pps=1"
        print(f"Or running with test URL: {test_url}")
        url = test_url
    else:
        url = sys.argv[1]
        
    result = fetch_ingredients(url)
    if result:
        print("\n--- Scraped Data ---")
        print(f"Product: {result['Product Name']}")
        print(f"Ingredients: {result['Ingredients']}")
        
        # Save to CSV
        filename = 'nykaa_ingredients.csv'
        write_header = not os.path.exists(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Product Name', 'Ingredients', 'URL'])
            if write_header:
                writer.writeheader()
            writer.writerow(result)
        print(f"\nSaved to {filename}")
    else:
        print("\nFailed to extract ingredients.")

if __name__ == "__main__":
    main()
