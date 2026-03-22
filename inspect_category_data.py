import json

print("Loading category_state.json...")
with open('category_state.json', 'r') as f:
    data = json.load(f)

categoryListing = data.get('categoryListing', {})
print("\nKeys in categoryListing:")
print(list(categoryListing.keys()))

products = categoryListing.get('products', [])
print(f"\nNumber of products found: {len(products)}")

if products:
    print("\nFirst Product Data (Sample):")
    p = products[0]
    # Print keys of first product
    print(f"Product Keys: {list(p.keys())}")
    for k, v in p.items():
        # Print some interesting fields
        if k in ['id', 'name', 'slug', 'url', 'productUrl', 'sku', 'link']:
            print(f"  {k}: {v}")
            
    print("\nAttempting to construct URL for first product:")
    # Look for URL structure
    url = p.get('url') or p.get('productUrl') or p.get('slug')
    print(f"  Extracted URL: {url}")

pagination = categoryListing.get('pagination', {})
print(f"\nPagination Data: {pagination}")
