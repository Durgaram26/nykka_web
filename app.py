from flask import Flask, render_template, jsonify, request
import os
import sys

# Add current directory to path so import works
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nykaa_list_scraper import scrape_category_and_ingredients

app = Flask(__name__)

CATEGORY_URLS = {
    'Face Moisturizer & Day Cream': 'https://www.nykaa.com/skin/moisturizers/face-moisturizer-day-cream/c/8394',
    'Night Cream': 'https://www.nykaa.com/skin/moisturizers/night-cream/c/8395',
    'Face Oils': 'https://www.nykaa.com/skin/moisturizers/face-oils/c/8396',
    'Face Wash': 'https://www.nykaa.com/skin/cleansers/face-wash/c/8378',
    'Serums & Essence': 'https://www.nykaa.com/skin/serums-essence/c/8390'
}

import re

def extract_category_name(url):
    """Extracts a neat category name from Nykaa URL."""
    match = re.search(r'/([^/]+)/c/\d+', url)
    if match:
        return match.group(1).replace('-', ' ').title()
    return "Custom Category"

@app.route('/')
def index():
    """Renders Dashboard."""
    return render_template('index.html', categories=CATEGORY_URLS.keys())

@app.route('/scrape', methods=['POST'])
def scrape():
    """Endpoint to trigger scraping."""
    category = request.form.get('category')
    custom_url = request.form.get('custom_url')
    max_pages = request.form.get('pages', 1, type=int)
    delay = request.form.get('delay', 1, type=float)
    
    # Determine URL and Name
    if custom_url:
        category_url = custom_url
        category_name = extract_category_name(custom_url)
    else:
        category_url = CATEGORY_URLS.get(category)
        category_name = category
        
    if not category_url:
        return jsonify({'status': 'error', 'message': 'Invalid category or URL'}), 400
        
    csv_file = "data/nykaa_ingredients_realtime.csv"
    print(f"Scraping triggered: {category_name} -> {category_url}")
    
    try:
        results = scrape_category_and_ingredients(category_url, max_pages=max_pages, delay=delay, csv_filename=csv_file, category_name=category_name)
        with_ingredients = sum(1 for item in results if item.get('ingredients') != "Not Found")
        
        return jsonify({
            'status': 'success',
            'category': category_name,
            'count': len(results),
            'with_ingredients': with_ingredients,
            'data': results
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/view_saved')
def view_saved():
    """Reads the CSV file and returns filtered data."""
    selected_category = request.args.get('category')
    csv_file = "data/nykaa_ingredients_realtime.csv"
    data = []
    
    if os.path.exists(csv_file):
        import csv
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filter by category if specified
                if not selected_category or selected_category == 'view_all' or row.get('category') == selected_category:
                    data.append(row)
    
    with_ingredients = sum(1 for item in data if item.get('ingredients') != "Not Found")
    
    return jsonify({
        'status': 'success',
        'category': selected_category or 'All',
        'count': len(data),
        'with_ingredients': with_ingredients,
        'data': data
    })

from flask import send_file

@app.route('/download')
def download():
    """Endpoint to download the CSV file."""
    csv_file = "data/nykaa_ingredients_realtime.csv"
    if os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name="nykaa_ingredients.csv")
    return jsonify({'status': 'error', 'message': 'No data saved yet.'}), 404

if __name__ == '__main__':
    # Run on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=True)
