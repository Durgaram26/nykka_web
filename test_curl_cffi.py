try:
    from curl_cffi import requests
    import json

    url = "https://www.nykaa.com/gateway-api/products/22032/reviews?pageNo=1&filters=DEFAULT&domain=nykaa"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.nykaa.com/cetaphil-cleansing-lotion/reviews/22032?skuId=22031&ptype=reviews',
    }

    print(f"Fetching {url} using curl_cffi...")
    # 'chrome' impersonate is the key to bypassing Cloudflare/Akamai
    response = requests.get(url, headers=headers, impersonate="chrome120")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("\n--- Success! ---")
        print(f"Found {len(data.get('response', {}).get('reviewData', []))} reviews.")
        # Print first review title
        if data.get('response', {}).get('reviewData'):
            print(f"First review: {data['response']['reviewData'][0].get('title')}")
    else:
        print(f"Failed to fetch. Content: {response.text[:200]}")

except Exception as e:
    print(f"Error: {e}")
