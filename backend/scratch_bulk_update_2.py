import json
import time
import subprocess
import os

INDEX_PATH = "search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

items = data.get("stored_items", [])

# Define rules as (base_code_prefix, variants_list, new_price)
update_rules = [
    ("2592", ["BRG", "BG", "GG", "MB", "RG"], 35750),
    ("2562", ["BRG", "BG", "GG", "MB", "RG"], 29500),
    ("2569", ["BRG", "BG"], 145000),
    ("2102", ["BRG", "BG", "MB", "RG", "GG"], 24500),
]

updated_count = 0

for rule in update_rules:
    prefix, variants, price = rule
    variants_upper = [v.upper() for v in variants]
    
    for item in items:
        if item.get("brand") != "Aquant":
            continue
            
        base_code = str(item.get("base_code") or "")
        search_code = str(item.get("search_code") or "")
        
        # Match base_code or search_code starting with prefix
        if base_code.startswith(prefix) or search_code.startswith(prefix):
            for variant in variants_upper:
                if search_code.endswith(f" {variant}") or search_code.endswith(f"-{variant}") or search_code == f"{base_code}{variant}":
                    orig_price = item.get("price")
                    # Match type
                    if isinstance(orig_price, int):
                        price_val = int(price)
                    elif isinstance(orig_price, float):
                        price_val = float(price)
                    else:
                        price_val = str(price)
                        
                    old_price_str = str(orig_price)
                    item['price'] = price_val
                    if 'mrp' in item:
                        item['mrp'] = price_val
                    if item.get('text') and old_price_str:
                        item['text'] = item['text'].replace(old_price_str, str(price))
                        
                    print(f"Updated {search_code}: {orig_price} -> {price_val}")
                    updated_count += 1

print(f"\nTotal items updated: {updated_count}")

if updated_count > 0:
    data['version'] = str(int(time.time()))
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved updated index locally.")
    
    print("Running direct_mongo_push.py...")
    res = subprocess.run(["venv/Scripts/python.exe", "direct_mongo_push.py"], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)
else:
    print("No items updated.")
