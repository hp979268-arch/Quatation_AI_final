import json
data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
for i in items:
    if isinstance(i, dict) and '30520' in str(i.get('search_code', '')):
        print(f"Search Code: {i.get('search_code')}")
        print(f"Name: {i.get('name')}")
        print(f"Price: {i.get('price')}")
        print(f"Images: {i.get('images')}")
        print("---")
