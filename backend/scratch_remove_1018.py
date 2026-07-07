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
    
    original_len = len(items)
    # Remove the exact item we added previously
    new_items = [item for item in items if item.get("search_code", "") != "1018 - FT"]
    
    if len(new_items) < original_len:
        print(f"Removed {original_len - len(new_items)} items!")
        
        # We need to rebuild the index without it
        search_engine.stored_items = []
        search_engine.keyword_index = {}
        search_engine.add_to_index(None, new_items)
        
        if mongodb.is_enabled():
            print("Pushing updated index to MongoDB Cloud...")
            data = {
                "stored_items": search_engine.stored_items,
                "keyword_index": search_engine.keyword_index
            }
            mongodb.save_search_index(data)
            print("Successfully synced to MongoDB!")
            
            try:
                urllib.request.urlopen("https://quotation-ai-backend-dn5t.onrender.com/refresh").read()
                print("Successfully triggered live backend refresh!")
            except Exception as e:
                print("Failed to trigger live backend refresh:", e)
    else:
        print("Item 1018 - FT not found.")

if __name__ == "__main__":
    main()
