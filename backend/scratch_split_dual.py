import os
import json
from PIL import Image

def split_dual_images(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # K-9301 is the LEFT image (wider)
    # K-9302 is the RIGHT image (narrower)
    
    # Actually, let's just split down the middle!
    # Left 50% = 9301
    # Right 50% = 9302
    
    # List of dual images by color
    colors = ['CP', 'AF', 'BV', 'RGD', 'BRD']
    
    for color in colors:
        # The base dual image is usually the _v3 image of 9301 or 9302
        # Let's find one that exists
        img_path = None
        for code in [f'K-9301IN-CL-{color}', f'K-9302IN-CL-{color}']:
            p = f'backend/static/images/Kohler/{code}_v3.png'
            if os.path.exists(p):
                img_path = p
                break
        
        if not img_path:
            continue
            
        print(f"Processing dual image for {color}: {img_path}")
        
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                
                # Check if it looks like a dual image (aspect ratio usually wide)
                # If width > height * 1.5, it's probably wide
                
                left_box = (0, 0, width // 2, height)
                right_box = (width // 2, 0, width, height)
                
                img_9301 = img.crop(left_box)
                img_9302 = img.crop(right_box)
                
                # Save them as _FINAL.png
                path_9301 = f'backend/static/images/Kohler/K-9301IN-CL-{color}_FINAL.png'
                path_9302 = f'backend/static/images/Kohler/K-9302IN-CL-{color}_FINAL.png'
                
                img_9301.save(path_9301)
                img_9302.save(path_9302)
                
                print(f"Saved {path_9301} and {path_9302}")
                
                # Update index
                for item in data['stored_items']:
                    if item.get('search_code') == f'K-9301IN-CL-{color}':
                        item['images'] = [f'/static/images/Kohler/K-9301IN-CL-{color}_FINAL.png']
                    elif item.get('search_code') == f'K-9302IN-CL-{color}':
                        item['images'] = [f'/static/images/Kohler/K-9302IN-CL-{color}_FINAL.png']
                        
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Done splitting images. Updating MongoDB...")
    from mongodb import get_db
    db = get_db()
    if db is not None:
        db.search_index_v2.replace_one({}, data, upsert=True)
        print("MongoDB updated.")

if __name__ == '__main__':
    split_dual_images('backend/search_index_v2.json')
