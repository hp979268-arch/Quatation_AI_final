
import json
import copy
import time

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])

# Find a template 1017 item
template = None
for item in items:
    if isinstance(item, dict) and item.get('base_code') == '1017' and item.get('variant_code') == 'AB':
        template = item
        break

if template:
    missing = ['BG', 'BRG', 'GG', 'MB', 'RG']
    labels = {'BG': 'Brushed Gold', 'BRG': 'Brushed Rose Gold', 'GG': 'Graphite Grey', 'MB': 'Matt Black', 'RG': 'Rose Gold'}
    added = 0
    for v in missing:
        # Check if already exists
        exists = any(i.get('base_code') == '1017' and i.get('variant_code') == v for i in items if isinstance(i, dict))
        if not exists:
            new_item = copy.deepcopy(template)
            new_item['variant_code'] = v
            new_item['search_code'] = f'1017 {v}'
            new_item['name'] = f'1017 {v} - {labels[v]}'
            new_item['text'] = f'1017 {v} - {labels[v]}\n{labels[v]}\n1017 {v}'
            new_item['finish_label'] = labels[v]
            # using cache bust ?v=7 as in template
            new_item['images'] = [f'/static/images/Aquant/1017{v}.png?v=7']
            items.append(new_item)
            added += 1

    if added > 0:
        with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))
        print(f'Added {added} missing 1017 variants.')
    else:
        print('Variants already exist.')
else:
    print('Template 1017 AB not found.')

