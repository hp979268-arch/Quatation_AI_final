import json

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['stored_items']
changes = 0

for p in products:
    code = str(p.get('search_code', ''))
    
    # Fix K-38896IN-4FS-BV price
    if code == 'K-38896IN-4FS-BV':
        if str(p.get('price')) == '14':
            p['price'] = '14200'
            changes += 1
            print(f"Fixed {code} price to 14200")

    # Fix K-30520IN-0 duplicate / names
    if code == 'K-30520IN-0':
        price = str(p.get('price', '')).replace('.00', '')
        if price == '13100':
            p['name'] = "K-30520IN-0 + K-8705IN-0 - Full Pedestal Wall Mount Basin Bundle"
            changes += 1
        elif price == '12400':
            p['name'] = "K-30520IN-0 + K-5584IN-0 - Half Pedestal Wall Mount Basin Bundle"
            changes += 1
        elif price == '10500':
            p['name'] = "K-30520IN-0 - Trace Rectangular Wall Mount Basin (Basin Only)"
            changes += 1

if changes > 0:
    data['version'] = data.get('version', 1) + 1
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"Saved {changes} changes to index. Version bumped.")
else:
    print("No changes made.")
