import json
import os

def restore_trim_valve():
    with open('backend/search_index_v2.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    img_dir = "backend/static/images/Kohler"
    count = 0
    
    # Get all _v2.png files
    v2_files = [f for f in os.listdir(img_dir) if f.endswith('_v2.png')]
    v2_codes = {f.replace('_v2.png', ''): f for f in v2_files}
    
    for item in db['stored_items']:
        if item.get('brand') == 'Kohler':
            code = item['search_code']
            parts = code.split(' + ')
            trim_code = parts[0].strip()
            
            if trim_code in v2_codes:
                item['images'] = [f"/static/images/Kohler/{v2_codes[trim_code]}?v=8"]
                count += 1
                print(f"Restored {code} to {v2_codes[trim_code]}")
            elif "trim" in str(item.get('description', '')).lower() and "valve" in str(item.get('description', '')).lower():
                print(f"Missed: {code}")
                
    print(f"Restored {count} Trim + Valve images from _v2.")
    
    if count > 0:
        with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
            
        from mongodb import get_db
        mongo = get_db()
        if mongo is not None:
            mongo.search_index_v2.replace_one({}, db, upsert=True)
            print("MongoDB updated.")

if __name__ == '__main__':
    restore_trim_valve()
