
import json
import time

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])

ts = int(time.time())

for item in items:
    if isinstance(item, dict) and 'K-30520IN-0' in item.get('search_code', ''):
        name = item.get('name', '')
        # Fix search_code
        if 'Full Pedestal' in name:
            item['search_code'] = 'K-30520IN-0 + K-8705IN-0'
            item['images'] = [f'/static/images/Kohler/K-30520IN-0_TraceFullPedestal.png?v={ts}']
        elif 'Half Pedestal' in name:
            item['search_code'] = 'K-30520IN-0 + K-5584IN-0'
            item['images'] = [f'/static/images/Kohler/K-30520IN-0_TraceHalfPedestal.png?v={ts}']
        elif 'Basin Only' in name:
            item['images'] = [f'/static/images/Kohler/K-30520IN-0.png?v={ts}']

with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))
print('Fixed search codes and images for K-30520IN-0 bundles.')

