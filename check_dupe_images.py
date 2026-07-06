import json
import collections
import os

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])

duplicate_search_codes = collections.defaultdict(list)
for item in items:
    if not isinstance(item, dict): continue
    sc = item.get('search_code')
    if sc:
        duplicate_search_codes[sc].append(item)

dupes = {k: v for k, v in duplicate_search_codes.items() if len(v) > 1}

base_dir = r'c:\Movies\quotation-ai\quotation-ai\backend'
bad_images = []

for k, v in dupes.items():
    for x in v:
        images = x.get('images', [])
        is_bad = False
        reason = ''
        if not images:
            is_bad = True
            reason = 'Empty image list'
        else:
            for img in images:
                if 'image_not_found' in img or not img.strip():
                    is_bad = True
                    reason = 'Placeholder or empty string'
                    break
                
                # Check if file exists
                rel_path = img.split('?')[0]
                if rel_path.startswith('/static/'):
                    rel_path = rel_path.replace('/static/', 'static/', 1)
                elif rel_path.startswith('/'):
                    rel_path = rel_path.lstrip('/')
                
                full_path = os.path.join(base_dir, rel_path)
                if not os.path.exists(full_path):
                    is_bad = True
                    reason = f'File not found: {rel_path}'
                    break
        
        if is_bad:
            bad_images.append({'code': k, 'price': x.get('price'), 'reason': reason, 'img': images})

if bad_images:
    print('Found broken images:')
    for b in bad_images:
        print(f"- {b['code']} (Price: {b['price']}): {b['reason']} | Current Img: {b['img']}")
else:
    print('All duplicate products have valid, existing image paths!')
