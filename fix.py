
import json
data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
changed = 0
v1017 = []
for item in items:
    if isinstance(item, dict):
        if item.get('base_code') == '1505' and item.get('variant_code') == 'G':
            item['price'] = '15250'
            changed += 1
        elif item.get('base_code') == '1017':
            v1017.append(item.get('variant_code', 'EMPTY') + ' - ' + str(item.get('price')))
if changed > 0:
    with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
print(f'Fixed {changed} items for 1505 G.')
print('1017 variants in index:', list(set(v1017)))

