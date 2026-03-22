import subprocess
import time
import requests
import os

print("1. Starting app.py in background...")
venv_python = "/media/durga/New Volume/Iink/.venv/bin/python"
process = subprocess.Popen([venv_python, "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(3)  # Wait for boot

try:
    # Test GET /
    print("\n2. Testing GET / with Categories...")
    r_get = requests.get("http://localhost:5000/")
    if r_get.status_code == 200:
        if "Face Moisturizer & Day Cream" in r_get.text:
            print("   ✅ Success: Categories are rendered in index.html.")
        else:
            print("   ❌ Fail: Categories not found in index.html.")

    # Test POST /scrape with Category
    print("\n3. Testing POST /scrape with Category selection...")
    post_data = {
        'category': 'Face Moisturizer & Day Cream',
        'pages': 1,
        'delay': 0.5
    }
    r_post = requests.post("http://localhost:5000/scrape", data=post_data, timeout=60)
    if r_post.status_code == 200:
        data = r_post.json()
        print(f"   ✅ Success: Scraped status: {data.get('status')}")
        print(f"   Total Count: {data.get('count')}")
        print(f"   With Ingredients: {data.get('with_ingredients')}")
    else:
        print(f"   ❌ Fail /scrape: {r_post.status_code}")

    # Test GET /view_saved
    print("\n4. Testing GET /view_saved...")
    r_view = requests.get("http://localhost:5000/view_saved")
    if r_view.status_code == 200:
        data = r_view.json()
        print(f"   ✅ Success: /view_saved status: {data.get('status')}")
        print(f"   Saved Count: {data.get('count')}")
        print(f"   With Ingredients in Saved: {data.get('with_ingredients')}")
    else:
        print(f"   ❌ Fail /view_saved: {r_view.status_code}")

finally:
    print("\n5. Stopping Flask Server...")
    process.terminate()
    process.wait()
    print("   Server stopped.")
