import json

INDEX_PATH = "search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

items = data.get("stored_items", [])
query = "1125"

matches = []
for idx, item in enumerate(items):
    code = str(item.get("base_code") or "")
    search_code = str(item.get("search_code") or "")
    name = str(item.get("name") or "")
    
    if query in code or query in search_code:
        matches.append((idx, item))

print(f"Found {len(matches)} matches:")
for idx, item in matches:
    print(f"Index: {idx} | Brand: {item.get('brand')} | BaseCode: {item.get('base_code')} | SearchCode: {item.get('search_code')} | Name: {item.get('name')} | Price: {item.get('price')}")
