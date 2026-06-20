import json
import os

def assign_final_images():
    with open('backend/search_index_v2.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    img_dir = "backend/static/images/Kohler"
    count = 0
    
    final_files = [f for f in os.listdir(img_dir) if f.endswith('_FINAL.png')]
    final_codes = {f.replace('_FINAL.png', ''): f for f in final_files}
    
    for item in db['stored_items']:
        if item.get('brand') == 'Kohler':
            code = item['search_code']
            parts = code.split(' + ')
            trim_code = parts[0].strip()
            
            # If it has a _FINAL image available
            if trim_code in final_codes:
                item['images'] = [f"/static/images/Kohler/{final_codes[trim_code]}?v=10"]
                count += 1
                
    print(f"Assigned {count} Trim + Valve images to _FINAL.")
    
    if count > 0:
        with open('backend/search_index_v2.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
            
        from backend.mongodb import get_db
        mongo = get_db()
        if mongo is not None:
            mongo.search_index_v2.replace_one({}, db, upsert=True)
            print("MongoDB updated.")

if __name__ == '__main__':
    assign_final_images()
