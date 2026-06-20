import sys
import os
import json

sys.path.append(os.path.abspath('backend'))
import search_engine

search_engine.load_index()

d = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
for i in d['stored_items']:
    if '30318IN BL' in str(i.get('search_code', '')):
        print(f"Testing {i['search_code']}")
        img = search_engine._best_item_image(i)
        print("RESULT:", img)
        print("CACHE for K-30318IN:", search_engine._resolved_code_to_image_cache.get("K-30318IN"))
