import json
from curl_cffi import requests
from bs4 import BeautifulSoup

url = "https://www.nykaa.com/cetaphil-cleansing-lotion/p/22032?skuId=22031"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers, impersonate="chrome120")

if response.status_code == 200:
    print("Success 200 OK")
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if script_tag:
        try:
            data = json.loads(script_tag.string)
            print("Found __NEXT_DATA__ JSON.")
            # Let's save it to a file to inspect keys
            with open('next_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("Saved __NEXT_DATA__ to next_data.json.")
            
            # Print top level keys
            print(f"Keys: {data.keys()}")
            if 'props' in data:
                 print(f"Props keys: {data['props'].keys()}")
                 if 'pageProps' in data['props']:
                      print(f"pageProps keys: {data['props']['pageProps'].keys()}")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
    else:
        print("Could not find __NEXT_DATA__ script tag.")
else:
    print(f"Failed with status: {response.status_code}")
