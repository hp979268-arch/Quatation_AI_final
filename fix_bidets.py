
import json
from collections import defaultdict

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])

codes_to_fix = ['K-28362IN-2-0', 'K-28820IN-0', 'K-4108IN-0', 'K-8297IN-0', 'K-32387IN-0']

grouped = defaultdict(list)
new_items = []

for i in items:
    if isinstance(i, dict) and i.get('search_code') in codes_to_fix:
        grouped[i.get('search_code')].append(i)
    else:
        new_items.append(i)

removed = 0
for code, group in grouped.items():
    # sort descending by price
    group.sort(key=lambda x: float(x.get('price', 0)), reverse=True)
    # append only the first (highest price)
    new_items.append(group[0])
    removed += len(group) - 1

data['stored_items'] = new_items
with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))

print(f'Removed {removed} wrong lower-priced bidet entries.')

