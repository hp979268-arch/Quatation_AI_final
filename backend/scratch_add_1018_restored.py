import sys
import os
import urllib.request

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine
import mongodb

def main():
    items_to_add = [
        {
            "text": "1018 - FT\nWaste Coupling\nSize: 32mm*175mm\nMRP : ₹ 2150.00/-",
            "name": "1018 - FT - Waste Coupling",
            "price": "2150",
            "images": [
                "/static/images/Aquant/1001.png?v=9"
            ],
            "brand": "Aquant",
            "category": "Waste Coupling",
            "base_code": "1018",
            "search_code": "1018 - FT",
            "source": "Manual Addition"
        }
    ]

    print("Loading search index from MongoDB...")
    search_engine.load_index(force=True)
    
    # Check if 1018 - FT already exists
    existing = False
    for item in search_engine.stored_items:
        if item.get("search_code") == "1018 - FT":
            print("Item already exists, updating it...")
            item.update(items_to_add[0])
            existing = True
            break
            
    if not existing:
        print(f"Adding 1 item to search engine...")
        search_engine.add_to_index(None, items_to_add)
    
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
        print("Warning: MongoDB is not enabled.")

if __name__ == "__main__":
    main()
