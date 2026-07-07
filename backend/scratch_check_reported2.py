import json

data=json.load(open('search_index_v2.json', 'r', encoding='utf-8-sig'))
target=['2592', '2562', '2569', '2104', '2106', '2102', '1411', '1415', '1418', '1320', '1437', '1155', '1485']

for item in data.get('stored_items', []):
    bc = str(item.get('base_code', ''))
    name = str(item.get('name', ''))
    sc = str(item.get('search_code', ''))
    if any(t in bc or t in name or t in sc for t in target) and item.get('brand') == 'Aquant':
        print(f"{item.get('search_code', name)} - Price: {item.get('price')} - Page: {item.get('page')}")
