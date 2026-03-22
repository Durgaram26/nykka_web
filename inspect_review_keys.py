from curl_cffi import requests
import json

url = "https://www.nykaa.com/gateway-api/products/22032/reviews?pageNo=1&filters=DEFAULT&domain=nykaa"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers, impersonate="chrome120")
if response.status_code == 200:
    data = response.json()
    reviews = data.get('response', {}).get('reviewData', [])
    if reviews:
        print("Keys in review objects:")
        print(list(reviews[0].keys()))
        # Print the first review fully
        print("\nFirst review full object:")
        print(json.dumps(reviews[0], indent=2))
    else:
        print("No reviews found.")
else:
    print(f"Failed with status: {response.status_code}")
