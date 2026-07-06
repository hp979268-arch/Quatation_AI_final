import json

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])

changed = 0
for item in items:
    if isinstance(item, dict) and item.get('search_code') == 'K-30520IN-0':
        name = item.get('name', '')
        if 'Full Pedestal' in name:
            item['images'] = ['/static/images/Kohler/K-30520IN-0_TraceFullPedestal.png?v=37']
            changed += 1
        elif 'Half Pedestal' in name:
            item['images'] = ['/static/images/Kohler/K-30520IN-0_TraceHalfPedestal.png?v=37']
            changed += 1

if changed > 0:
    with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
    print(f'Fixed {changed} K-30520IN-0 images.')
