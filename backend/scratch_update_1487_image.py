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
    
    fixed = False
    for item in items:
        # Check if the code is 1487
        search_code = item.get("search_code", "")
        base_code = item.get("base_code", "")
        if "1487" == search_code or "1487" == base_code:
            item["images"] = ["/static/images/Aquant/1487-2.png"]
            print(f"Updated 1487 ({item.get('name')}) with images: {item['images']}")
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
        print("Could not find item 1487 to update.")

if __name__ == "__main__":
    main()
