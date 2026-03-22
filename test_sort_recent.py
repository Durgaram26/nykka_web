from curl_cffi import requests
import json

# Test with sort=MOST_RECENT
url = "https://www.nykaa.com/gateway-api/products/22032/reviews?pageNo=1&sort=MOST_RECENT&domain=nykaa"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers, impersonate="chrome120")

if response.status_code == 200:
    data = response.json()
    reviews = data.get('response', {}).get('reviewData', [])
    if reviews:
        print(f"Found {len(reviews)} reviews.")
        ratings = [r.get('rating') for r in reviews]
        print(f"Ratings on Page 1: {ratings}")
        # Count non-5 stars
        non_five = [r for r in reviews if r.get('rating') != 5]
        print(f"Non-5 star reviews count: {len(non_five)}")
    else:
        print("No reviews found.")
else:
    print(f"Failed with status: {response.status_code}")
