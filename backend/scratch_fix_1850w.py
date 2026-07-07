import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine

def main():
    print("Loading local JSON file...")
    with open("search_index_v2.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        items = data.get("stored_items", [])
        
    print(f"Total items in local JSON: {len(items)}")
    
    found = []
    for item in items:
        text = item.get("text", "")
        if "1850 W" in text and text.startswith("Extra - "):
            found.append(item)

    print(f"Found {len(found)} matching items locally.")
    
    fixed_count = 0
    for item in found:
        text = item.get("text", "")
        old_name = item.get("name", "")
        first_line = text.split("\n")[0].strip()
        
        new_name = f"{first_line} (1850 W - SmartElite)"
        new_code = item.get("search_code", "")
        if "Extra" not in new_code:
            new_code = f"Extra {new_code}"
             
        if old_name != new_name or new_code != item.get("search_code"):
            print(f"Updating locally: '{old_name}' -> '{new_name}'")
            item["name"] = new_name
            item["search_code"] = new_code
            fixed_count += 1
                
    if fixed_count > 0:
        print(f"Fixed {fixed_count} items. Pushing this data to MongoDB...")
        # To push, we can just replace search_engine.stored_items and call save_index
        search_engine.stored_items = items
        # Rebuild keyword index
        search_engine.keyword_index = {}
        # Wait, add_to_index handles keyword indexing and saving.
        search_engine.stored_items = []
        search_engine.keyword_index = {}
        search_engine.add_to_index(None, items)
        print("Done!")

if __name__ == "__main__":
    main()
