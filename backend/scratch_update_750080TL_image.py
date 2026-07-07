import sys
import os
import urllib.request

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine
import mongodb

def main():
    print("Loading search index from MongoDB...")
    search_engine.load_index(force=True)
    items = search_engine.stored_items
    
    # 1. Find item 60080TL and get its images
    image_to_use = None
    for item in items:
        search_code = item.get("search_code", "")
        base_code = item.get("base_code", "")
        if "60080TL" in search_code or "60080TL" in base_code:
            image_to_use = item.get("images", [])
            print(f"Found item 60080TL ({item.get('name')}). Images: {image_to_use}")
            break
            
    if not image_to_use:
        print("Could not find an item with code 60080TL!")
        return
        
    # 2. Apply it to 750080TL
    fixed = False
    for item in items:
        search_code = item.get("search_code", "")
        base_code = item.get("base_code", "")
        if "750080TL" in search_code or "750080TL" in base_code:
            item["images"] = image_to_use
            print(f"Updated 750080TL ({item.get('name')}) with images: {item['images']}")
            fixed = True
            
    if fixed:
        if mongodb.is_enabled():
            print("Pushing updated index to MongoDB Cloud...")
            data = {
                "stored_items": search_engine.stored_items,
                "keyword_index": search_engine.keyword_index
            }
            mongodb.save_search_index(data)
            print("Successfully synced to MongoDB!")
            
            # Hit the refresh endpoint
            try:
                urllib.request.urlopen("https://quotation-ai-backend-dn5t.onrender.com/refresh").read()
                print("Successfully triggered live backend refresh!")
            except Exception as e:
                print("Failed to trigger live backend refresh:", e)
    else:
        print("Could not find item 750080TL to update.")

if __name__ == "__main__":
    main()
