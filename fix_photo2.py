
import json
import time

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])
ts = int(time.time())

for i in items:
    if isinstance(i, dict) and i.get('search_code') == 'K-28362IN-2-0':
        images = i.get('images', [])
        new_imgs = []
        for img in images:
            base = img.split('?')[0]
            new_imgs.append(f'{base}?v={ts}')
        i['images'] = new_imgs

with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))
print('Applied cache buster to K-28362IN-2-0')

