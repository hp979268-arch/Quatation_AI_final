import json
from mongodb import get_db
from dotenv import load_dotenv
load_dotenv()

with open('search_index_v2.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for item in db['stored_items']:
    code = item.get('search_code', '')
    if '9301IN-CL' in code or '9302IN-CL' in code:
        if item.get('images'):
            item['images'] = [item['images'][0].replace('_FINAL.png', '_v3.png')]

with open('search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

mongo_db = get_db()
if mongo_db is not None:
    mongo_db.search_index_v2.replace_one({}, db, upsert=True)
    print("Reverted in MongoDB")
else:
    print("Failed to connect to MongoDB")
