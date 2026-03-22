from bs4 import BeautifulSoup
import json
import re

print("Loading nykaa_page.html...")
with open('nykaa_page.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
scripts = soup.find_all('script')

for s in scripts:
    if s.string and '__PRELOADED_STATE__' in s.string:
         print("Found __PRELOADED_STATE__ script.")
         # Find the index of =
         idx = s.string.find('=')
         if idx != -1:
              json_str = s.string[idx+1:].strip()
              # Remove trailing semicolon if present
              if json_str.endswith(';'):
                   json_str = json_str[:-1]
              
              try:
                   data = json.loads(json_str)
                   print("Successfully parsed JSON!")
                   
                   # Recursive function to find key
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
                        
                   ingredients = find_key(data, 'ingredients')
                   if ingredients:
                        print(f"\nIngredients found (HTML):")
                        print(ingredients)
                        # Strip HTML tags
                        clean_ingredients = BeautifulSoup(ingredients, 'html.parser').get_text()
                        print(f"\nClean Ingredients List:")
                        print(clean_ingredients)
              except Exception as e:
                    print(f"Error parsing JSON: {e}")
         break
