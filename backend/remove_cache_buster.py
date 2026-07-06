import json

with open('c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

targets = ['K-1042534', 'K-1060831', 'K-1063956', 'K-1286731', 'K-17663IN-0', 'K-82958']

updated = 0
for item in d.get('stored_items',[]):
    if item.get('search_code') in targets:
        images = item.get('images', [])
        new_images = []
        for img in images:
            if '?v=' in img:
                img = img.split('?v=')[0]
                updated += 1
            new_images.append(img)
        item['images'] = new_images

if updated > 0:
    with open('c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print(f'Fixed {updated} image URLs.')
