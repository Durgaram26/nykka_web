import subprocess
import time
import requests
import os

print("1. Starting app.py in background...")
venv_python = "/media/durga/New Volume/Iink/.venv/bin/python"
process = subprocess.Popen([venv_python, "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(4)  # Wait for boot

try:
    # Test POST /scrape to populate CSV
    print("\n2. Scraping some items to populate CSV...")
    post_data = {'category': 'Night Cream', 'pages': 1, 'delay': 0.5}
    r = requests.post("http://localhost:5000/scrape", data=post_data, timeout=60)
    print(f"   Scrape Status: {r.status_code}")

    # Test GET /download
    print("\n3. Testing GET /download...")
    r_download = requests.get("http://localhost:5000/download")
    if r_download.status_code == 200:
        cd = r_download.headers.get('Content-Disposition')
        print(f"   ✅ Success: /download status: 200")
        print(f"   Content-Disposition: {cd}")
        if 'attachment' in cd and 'filename=' in cd:
             print("   ✅ Verification: Download header is correct.")
        else:
             print("   ❌ Verification: Missing attachment header.")
    else:
        print(f"   ❌ Fail /download: {r_download.status_code}")

finally:
    print("\n4. Stopping Flask Server...")
    process.terminate()
    process.wait()
    print("   Server stopped.")
