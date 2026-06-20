import json
import os

def restore_combined_images():
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    img_dir = "backend/static/images/Kohler"
    count = 0
    
    for item in db['stored_items']:
        if item.get('brand') == 'Kohler' and '+' in item.get('search_code', ''):
            code = item['search_code']
            # The combined image format is usually code.replace(' ', '_').replace('+', 'plus') + '_combined.png'
            # Or just code + '_combined.png'
            # Let's check common patterns
            possible_names = [
                f"{code}_combined.png",
                f"{code.replace(' ', '')}_combined.png",
                f"{code.replace('+', '_plus_')}_combined.png"
            ]
            
            # Also, some might have been saved as just the code name but replacing spaces/plus
            
            found = False
            for name in possible_names:
                if os.path.exists(os.path.join(img_dir, name)):
                    item['images'] = [f"/static/images/Kohler/{name}?v=7"]
                    found = True
                    count += 1
                    print(f"Restored {code} -> {name}")
                    break
                    
            if not found:
                # Search the directory for ANY file that contains '_combined' and parts of the code
                parts = code.split('+')
                p1 = parts[0].strip()
                for f in os.listdir(img_dir):
                    if '_combined.png' in f and p1 in f:
                        item['images'] = [f"/static/images/Kohler/{f}?v=7"]
                        found = True
                        count += 1
                        print(f"Fuzzy Restored {code} -> {f}")
                        break
                        
                if not found:
                    print(f"Could not find combined image for {code}")
                    
    print(f"Restored {count} combined images.")
    
    if count > 0:
        with open('search_index_v2.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
            
        from mongodb import get_db
        mongo = get_db()
        if mongo is not None:
            mongo.search_index_v2.replace_one({}, db, upsert=True)
            print("MongoDB updated.")

if __name__ == '__main__':
    restore_combined_images()
