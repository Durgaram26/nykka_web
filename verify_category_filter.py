import subprocess
import time
import requests
import os

print("1. Starting app.py in background...")
venv_python = "/media/durga/New Volume/Iink/.venv/bin/python"
process = subprocess.Popen([venv_python, "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(4)  # Wait for boot

try:
    # Test POST /scrape with Custom URL to verify Category extraction
    print("\n2. Testing POST /scrape with Custom URL category extraction...")
    post_data = {
        'custom_url': 'https://www.nykaa.com/skin/moisturizers/face-moisturizer-day-cream/c/8394',
        'pages': 1,
        'delay': 0.5
    }
    r_post = requests.post("http://localhost:5000/scrape", data=post_data, timeout=60)
    if r_post.status_code == 200:
        data = r_post.json()
        print(f"   ✅ Success: Scraped Category: {data.get('category')}")
        print(f"   Total Count: {data.get('count')}")
    else:
        print(f"   ❌ Fail /scrape custom: {r_post.status_code}")

    # Test POST /scrape with predefined category
    print("\n3. Testing POST /scrape with predefined category...")
    post_data2 = {
        'category': 'Night Cream',
        'pages': 1,
        'delay': 0.5
    }
    r_post2 = requests.post("http://localhost:5000/scrape", data=post_data2, timeout=60)
    if r_post2.status_code == 200:
        data2 = r_post2.json()
        print(f"   ✅ Success: Scraped Predefined Category: {data2.get('category')}")
    else:
         print(f"   ❌ Fail /scrape predefined: {r_post2.status_code}")

    # Test GET /view_saved FILTERED by Category
    print("\n4. Testing GET /view_saved FILTERED by Category ('Night Cream')...")
    r_view = requests.get("http://localhost:5000/view_saved?category=Night Cream")
    if r_view.status_code == 200:
        data = r_view.json()
        print(f"   ✅ Success: /view_saved status: {data.get('status')}")
        print(f"   Category Selected: {data.get('category')}")
        print(f"   Filtered Count: {data.get('count')}")
        # Verify all items belong to Night Cream
        all_match = all(item.get('category') == 'Night Cream' for item in data.get('data', []))
        if all_match and data.get('count') > 0:
             print("   ✅ Verification: All items match the requested category.")
        else:
             print("   ❌ Verification: Category filtering failed or no items found.")
    else:
        print(f"   ❌ Fail /view_saved: {r_view.status_code}")

    # Test GET /view_saved 'view_all'
    print("\n5. Testing GET /view_saved with 'view_all' filter...")
    r_view_all = requests.get("http://localhost:5000/view_saved?category=view_all")
    if r_view_all.status_code == 200:
        data_all = r_view_all.json()
        print(f"   ✅ Success: Loaded All Saved Items. Count: {data_all.get('count')}")
    else:
        print(f"   ❌ Fail /view_saved view_all: {r_view_all.status_code}")

finally:
    print("\n6. Stopping Flask Server...")
    process.terminate()
    process.wait()
    print("   Server stopped.")
