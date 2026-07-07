import json

with open("search_index_v2.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

items = data.get("stored_items", [])
matches = [item for item in items if "-AF" in str(item.get("search_code", ""))]

print(f"Found {len(matches)} matches with -AF:")
for item in matches[:10]:
    print(f"Brand: {item.get('brand')} | SearchCode: {item.get('search_code')} | Name: {item.get('name')} | Price: {item.get('price')}")
