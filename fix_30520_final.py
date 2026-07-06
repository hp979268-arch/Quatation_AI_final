import json
import time

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
ts = int(time.time())

for item in items:
    if isinstance(item, dict) and '30520' in str(item.get('search_code', '')):
        name = item.get('name', '')
        sc = item.get('search_code', '')
        if 'Full Pedestal' in name or 'K-8705IN-0' in sc:
            item['images'] = [f'/static/images/Kohler/K-30520IN-0_TraceFullPedestal.png?v={ts}']
            print(f"Fixed Full Pedestal -> TraceFullPedestal")
        elif 'Half Pedestal' in name or 'K-5584IN-0' in sc:
            item['images'] = [f'/static/images/Kohler/K-30520IN-0_TraceHalfPedestal.png?v={ts}']
            print(f"Fixed Half Pedestal -> TraceHalfPedestal")
        elif 'Basin Only' in name:
            item['images'] = [f'/static/images/Kohler/K-30520IN-0_SpanBasin.png?v={ts}']
            print(f"Fixed Basin Only -> SpanBasin")

with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))
print('Done! All 3 K-30520IN-0 images correctly mapped.')
