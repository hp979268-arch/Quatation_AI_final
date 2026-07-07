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
        if "750080 TL" == item.get("search_code", ""):
            item["images"] = ["/static/images/Aquant/750080TL.png"]
            item["image"] = "/static/images/Aquant/750080TL.png"
            print(f"Updated 750080 TL -> image: {item['image']}")
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
            
            try:
                urllib.request.urlopen("https://quotation-ai-backend-dn5t.onrender.com/refresh").read()
                print("Successfully triggered live backend refresh!")
            except Exception as e:
                print("Failed to trigger live backend refresh:", e)
    else:
        print("Could not find 750080 TL!")

if __name__ == "__main__":
    main()
