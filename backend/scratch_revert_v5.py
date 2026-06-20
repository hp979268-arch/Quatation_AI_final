import json
import os
from mongodb import get_db

with open('search_index_v2.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

changed_count = 0
for item in db['stored_items']:
    code = item.get('search_code', '')
    if code.startswith('K-274'):
        if item.get('images'):
            current_img = item['images'][0]
            if '_v5.png' in current_img:
                orig_img = current_img.replace('_v5.png', '.png')
                if os.path.exists('.' + orig_img):
                    item['images'] = [orig_img]
                    changed_count += 1
                    print(f"Reverted {code} back to original {orig_img}")
                else:
                    # try with space
                    orig_img_2 = current_img.replace('_v5.png', '').replace('-', ' ') + '.png'
                    if os.path.exists('.' + orig_img_2):
                        item['images'] = [orig_img_2]
                        changed_count += 1
                        print(f"Reverted {code} back to original {orig_img_2}")
                    else:
                        print(f"WARNING: No original image found for {code} ({orig_img})")

print(f"Changed {changed_count} items.")

with open('search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

mongo_db = get_db()
if mongo_db is not None:
    mongo_db.search_index_v2.replace_one({}, db, upsert=True)
    print("Updated MongoDB.")
