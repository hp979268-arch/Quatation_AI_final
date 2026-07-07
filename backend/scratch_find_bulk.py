import json

INDEX_PATH = "search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

items = data.get("stored_items", [])
models_to_check = ["2592", "2562", "2569", "2104", "2106", "2102", "1411", "1415", "1418", "1320", "1437", "1155", "1485"]

found_items = []
for idx, item in enumerate(items):
    code = str(item.get("base_code") or "")
    search_code = str(item.get("search_code") or "")
    
    # Check if any model string is present in code or search_code
    matched_model = None
    for model in models_to_check:
        if model in code or model in search_code:
            matched_model = model
            break
            
    if matched_model:
        found_items.append((idx, matched_model, item))

print(f"Total matched items: {len(found_items)}")
for idx, model, item in found_items:
    print(f"Model: {model} | Index: {idx} | Brand: {item.get('brand')} | BaseCode: {item.get('base_code')} | SearchCode: {item.get('search_code')} | Name: {item.get('name')} | Price: {item.get('price')}")
