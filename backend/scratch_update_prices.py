import json
import time
import subprocess
import os

INDEX_PATH = "search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

items = data.get("stored_items", [])
target_codes = ["1125 BRG", "1125 BG", "1125 MB", "1125 RG"]

updated_count = 0
for item in items:
    search_code = item.get("search_code")
    if search_code in target_codes:
        orig_price = item.get("price")
        # Match type of the original price
        if isinstance(orig_price, int):
            price_val = 4400
        elif isinstance(orig_price, float):
            price_val = 4400.0
        else:
            price_val = "4400"
            
        old_price_str = str(orig_price)
        
        item['price'] = price_val
        if 'mrp' in item:
            item['mrp'] = price_val
            
        if item.get('text') and old_price_str:
            item['text'] = item['text'].replace(old_price_str, "4400")
            
        print(f"Updated {search_code}: {orig_price} -> {price_val}")
        updated_count += 1

if updated_count > 0:
    # Bump version
    data['version'] = str(int(time.time()))
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved updated index locally.")
    
    # Run mongo push
    print("Running direct_mongo_push.py...")
    res = subprocess.run(["venv/Scripts/python.exe", "direct_mongo_push.py"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)
else:
    print("No items updated.")
