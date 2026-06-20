import json

with open('search_index_v2.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for item in db['stored_items']:
    if item.get('images'):
        new_images = []
        for img in item['images']:
            # remove old query param
            if '?' in img:
                img = img.split('?')[0]
            # append new query param
            img += '?v=6'
            new_images.append(img)
        item['images'] = new_images

with open('search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

from mongodb import get_db
mongo = get_db()
if mongo is not None:
    mongo.search_index_v2.replace_one({}, db, upsert=True)
    print("MongoDB updated.")
