import json
data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
codes = ['K-28362IN-2-0', 'K-28820IN-0', 'K-4108IN-0', 'K-8297IN-0', 'K-32387IN-0']
for i in items:
    if isinstance(i, dict) and i.get('search_code') in codes:
        print(f"--- {i.get('search_code')} --- Price: {i.get('price')} \nRaw Text: {repr(i.get('text'))}")
