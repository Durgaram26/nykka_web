from curl_cffi import requests

url = "https://www.nykaa.com/cetaphil-cleansing-lotion/p/22032?skuId=22031"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers, impersonate="chrome120")

if response.status_code == 200:
    with open('nykaa_page.html', 'w', encoding='utf-8') as f:
         f.write(response.text)
    print("Saved HTML to nykaa_page.html")
    
    # Check if "Aqua" is in text
    if "Aqua" in response.text:
         print("'Aqua' found in response text!")
    else:
         print("'Aqua' NOT found in response text.")
else:
    print(f"Failed with status: {response.status_code}")
