import json
import os
import re
from PIL import Image
import sys

def normalize(text):
    if not text: return ""
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def split_words(text):
    if not text: return []
    words = re.split(r'[\s\-]+', str(text).lower())
    res = set()
    for w in words:
        clean = re.sub(r'[^a-z0-9]', '', w)
        if len(clean) >= 2:
            res.add(clean)
    return res

def clean_junk_entries(data):
    """Removes junk 1-2 digit entries like '30', '21' from search index."""
    items = data.get('stored_items', [])
    initial_count = len(items)
    
    new_items = []
    for item in items:
        code = item.get('search_code', '')
        # If code is just a number <= 3 digits and no alphabets, it's likely junk from PDF extraction
        if code.isdigit() and len(code) <= 3:
            continue
        new_items.append(item)
        
    data['stored_items'] = new_items
    print(f"[*] Cleaned {initial_count - len(new_items)} junk entries from database.")

def rebuild_keyword_index(data):
    """Rebuilds the keyword index mapping for robust search autocomplete."""
    print("[*] Rebuilding keyword index...")
    items = data.get('stored_items', [])
    keyword_index = {}
    
    for idx, item in enumerate(items):
        code = item.get('search_code', '')
        base_code = item.get('base_code', '')
        name = item.get('name', '')
        brand = item.get('brand', '')
        
        words = set()
        words.update(split_words(code))
        words.update(split_words(base_code))
        words.update(split_words(name))
        words.update(split_words(brand))
        
        # Add pure number variations (e.g. 22786 from K-22786IN)
        for c in [code, base_code]:
            if c:
                words.add(normalize(c))
                m = re.search(r'\d+', c)
                if m: words.add(m.group(0))
                
        for w in words:
            if not w: continue
            if w not in keyword_index:
                keyword_index[w] = []
            if idx not in keyword_index[w]:
                keyword_index[w].append(idx)
                
    data['keyword_index'] = keyword_index
    print(f"[*] Keyword index rebuilt with {len(keyword_index)} unique terms.")

def crop_multi_part_images(data):
    """Crops overly wide images (e.g. Trim+Valve shown side-by-side) into single thumbnails."""
    print("[*] Checking for wide multi-part images...")
    items = data.get('stored_items', [])
    cropped_count = 0
    
    for item in items:
        name = str(item.get('name', '')).lower()
        if 'trim' in name or 'bath and shower' in name or 'at 235' in name or 'at 360' in name or 'at ' in name:
            images = item.get('images', [])
            if not images: continue
            
            img_path = images[0].lstrip('/')
            if not os.path.exists(img_path): continue
                
            try:
                img = Image.open(img_path)
                w, h = img.size
                if w > h * 1.3: # Moderately wide, implies multiple items
                    crop_box = (0, 0, h, h)
                    cropped = img.crop(crop_box)
                    cropped.save(img_path)
                    cropped_count += 1
            except Exception as e:
                print(f"[!] Failed to process {img_path}: {e}")
                
    print(f"[*] Cropped {cropped_count} multi-part images to single thumbnails.")

def sync_to_mongodb(data):
    """Synchronizes the updated JSON index to MongoDB."""
    print("[*] Synchronizing with MongoDB...")
    try:
        from dotenv import load_dotenv
        load_dotenv('.env')
        import mongodb
        mongodb.save_search_index(data)
        print("[*] MongoDB synchronization successful.")
    except Exception as e:
        print(f"[!] MongoDB sync failed: {e}")

def run_maintenance():
    print("=== Quotation AI Maintenance Script ===")
    index_path = 'search_index_v2.json'
    
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    clean_junk_entries(data)
    rebuild_keyword_index(data)
    crop_multi_part_images(data)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Update local app data for electron app
    import shutil
    local_app_data = os.path.expandvars(r"%LOCALAPPDATA%\Shreeji Ceramica\search_index_v2.json")
    if os.path.exists(os.path.dirname(local_app_data)):
        shutil.copy2(index_path, local_app_data)
        print("[*] Updated local Electron App data.")
        
    sync_to_mongodb(data)
    print("=== Maintenance Complete ===")

if __name__ == '__main__':
    run_maintenance()
