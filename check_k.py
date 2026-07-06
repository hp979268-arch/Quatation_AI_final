import json
data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
for i in items:
    if isinstance(i, dict) and i.get('search_code') == 'K-30520IN-0':
        print(f"Name: {i.get('name')}\nPrice: {i.get('price')}\nImages: {i.get('images')}\n---")
