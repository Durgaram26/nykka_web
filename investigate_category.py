from curl_cffi import requests
from bs4 import BeautifulSoup
import json

url = "https://www.nykaa.com/skin/moisturizers/face-moisturizer-day-cream/c/8394"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print(f"Fetching {url}...")
try:
    response = requests.get(url, headers=headers, impersonate="chrome120")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        
        found = False
        for s in scripts:
            if s.string and '__PRELOADED_STATE__' in s.string:
                print("Found __PRELOADED_STATE__")
                idx = s.string.find('=')
                if idx != -1:
                    json_str = s.string[idx+1:].strip()
                    if json_str.endswith(';'):
                        json_str = json_str[:-1]
                    
                    try:
                        data = json.loads(json_str)
                        print("Keys in __PRELOADED_STATE__:")
                        print(list(data.keys()))
                        
                        # Save to file for deep inspection
                        with open('category_state.json', 'w') as f:
                            json.dump(data, f, indent=2)
                        print("Saved state to category_state.json")
                        found = True
                    except Exception as e:
                        print(f"JSON Parse Error: {e}")
                break
        
        if not found:
             print("__PRELOADED_STATE__ not found in script tags.")
             # Save HTML to inspect
             with open('category_page.html', 'wb') as f:
                  f.write(response.content)
             print("Saved HTML to category_page.html")
    else:
        print(f"Failed with status: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
