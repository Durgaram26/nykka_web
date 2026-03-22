import subprocess
import time
import requests
import os
import signal

print("1. Starting app.py in background...")
# Use the virtual environment Python
venv_python = "/media/durga/New Volume/Iink/.venv/bin/python"
process = subprocess.Popen([venv_python, "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for server to start
print("Waiting for server to start (3s)...")
time.sleep(3)

try:
    # 2. Test GET /
    print("\n2. Testing GET / (Home Page)...")
    try:
        r_get = requests.get("http://localhost:5000/", timeout=5)
        print(f"   Status Code: {r_get.status_code}")
        if r_get.status_code == 200 and "<html" in r_get.text:
            print("   ✅ Success: Home page loaded with HTML.")
        else:
            print("   ❌ Fail: Home page load failed.")
    except Exception as e:
         print(f"   ❌ Error GET /: {e}")

    # 3. Test POST /scrape (Test with 1 product link list limit if possible?)
    # Since we can't easily mock within the subprocess without editing files,
    # we'll test /scrape with default 1 page.
    print("\n3. Testing POST /scrape (1 Page)...")
    try:
        # Send POST with pages=1
        r_post = requests.post("http://localhost:5000/scrape", data={'pages': 1, 'delay': 0.5}, timeout=60)
        print(f"   Status Code: {r_post.status_code}")
        
        if r_post.status_code == 200:
            data = r_post.json()
            print(f"   ✅ Success: Scraped {data.get('status')} with count {data.get('count')}")
            if data.get('data'):
                print(f"   Sample Item: {data['data'][0]['name']}")
        else:
            print(f"   ❌ Fail status code: {r_post.status_code}")
            print(r_post.text[:200])
            
    except Exception as e:
         print(f"   ❌ Error POST /scrape: {e}")

finally:
    # 4. Terminate process
    print("\n4. Stopping Flask Server...")
    process.terminate()
    process.wait()
    print("   Server stopped.")
