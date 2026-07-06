"""Rebuild keyword index in-memory and push to MongoDB with updated search_engine logic."""
import json, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

import search_engine
import mongodb

# Load stored items from existing JSON
data = json.load(open('search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
print(f'Loaded {len(items)} items')

# Rebuild keyword index fresh
search_engine.stored_items = []
search_engine.keyword_index = {}
search_engine._keyword_keys_sorted.clear()
search_engine.item_code_meta_cache = {}

search_engine.add_to_index(None, items)
print(f'Rebuilt keyword index with {len(search_engine.keyword_index)} keys')

# Verify 30520 is indexed
test_keys = [k for k in search_engine.keyword_index if '30520' in k]
print(f'Keys containing 30520: {test_keys}')
indices = set()
for k in test_keys:
    indices.update(search_engine.keyword_index[k])
for i in indices:
    print(f'  -> {search_engine.stored_items[i].get("search_code")} | {search_engine.stored_items[i].get("name")}')

# Push to MongoDB
new_data = {'stored_items': search_engine.stored_items, 'keyword_index': search_engine.keyword_index}
with open('search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, separators=(',', ':'))

mongodb.save_search_index(new_data)
print(f'Pushed to MongoDB successfully!')
