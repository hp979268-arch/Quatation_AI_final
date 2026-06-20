import sys
import os
import json

sys.path.append(os.path.abspath('backend'))
import search_engine

search_engine.load_index()

d = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
for i in d['stored_items']:
    if i.get('search_code') == 'K-26297IN BL':
        print(f"Testing {i['search_code']}")
        img = search_engine._best_item_image(i)
        print("RESULT:", img)
