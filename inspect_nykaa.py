import requests
from bs4 import BeautifulSoup

url = "https://www.nykaa.com/cetaphil-cleansing-lotion/reviews/22032?skuId=22031&ptype=reviews"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching {url}...")
try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Let's find the review text we saw in the chunk
    search_text = "I'm using this brand since 2020"
    element = soup.find(string=lambda text: search_text in text if text else False)
    
    if element:
        print("\n--- Found Review Text ---")
        print(f"Text: {element.strip()}")
        print("\n--- Parent Elements ---")
        parent = element.parent
        for _ in range(5):
            if parent:
                print(f"Tag: {parent.name}, Class: {parent.get('class')}")
                parent = parent.parent
    else:
        print("\nReview text not found in source.")
        # Print a snippet of the body to see what's there
        print(soup.get_text()[:500])

    # Check for JSON data in script tags
    print("\n--- Checking for JSON in script tags ---")
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and ('__NEXT_DATA__' in script.string or 'window.__PRELOADED_STATE__' in script.string):
            print(f"Found script containing data!")
            # Print a snippet
            print(script.string[:500])
            break

except Exception as e:
    print(f"Error: {e}")
