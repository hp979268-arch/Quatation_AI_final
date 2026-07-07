import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine
import mongodb
import urllib.request

def main():
    print("Loading search index from MongoDB...")
    search_engine.load_index(force=True)
    items = search_engine.stored_items
    
    # 1. Find item 1001 and get its images
    image_to_use = None
    for item in items:
        # Check if the base code or search code contains 1001
        # It's better to check exact match or close match
        search_code = item.get("search_code", "")
        base_code = item.get("base_code", "")
        if search_code == "1001" or base_code == "1001" or "1001" in search_code.split():
            image_to_use = item.get("images", [])
            print(f"Found item 1001 ({item.get('name')}). Images: {image_to_use}")
            break
            
    if not image_to_use:
        print("Could not find an item with code 1001!")
        return
        
    # 2. Apply it to 1018 - FT
    fixed = False
    for item in items:
        if item.get("search_code") == "1018 - FT":
            item["images"] = image_to_use
            print(f"Updated 1018 - FT with images: {item['images']}")
            fixed = True
            break
            
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
        print("Could not find item 1018 - FT to update.")

if __name__ == "__main__":
    main()
