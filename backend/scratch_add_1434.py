import sys
import os
import json
import re

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine
import mongodb

def update_mrp_in_text(text, new_price):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "MRP" in line.upper() and "₹" in line:
            lines[i] = re.sub(r'₹\s*[\d,]+(?:\.\d+)?', f'₹ {new_price}.00', line)
    return "\n".join(lines)

def main():
    search_engine.load_index(force=True)
    items = search_engine.stored_items
    
    # Find 1434-900 MM to use as a template
    template_item = None
    for item in items:
        if "1434-900 MM" in item.get("search_code", ""):
            template_item = dict(item)  # Make a copy
            break
            
    if template_item:
        print("Found template: ", template_item.get("name"))
        
        # Modify it for 1200 MM
        new_item = dict(template_item)
        new_item['search_code'] = new_item['search_code'].replace("900", "1200")
        new_item['name'] = new_item['name'].replace("900", "1200")
        
        # Replace 900 with 1200 in the text block
        text = new_item.get('text', '')
        text = text.replace("900", "1200")
        new_item['text'] = update_mrp_in_text(text, "18250")
        new_item['price'] = "18250"
        
        print("Creating new item: ", new_item.get("name"), " with price ", new_item.get("price"))
        
        # Add to index
        search_engine.add_to_index(None, [new_item])
        
        if mongodb.is_enabled():
            print("Pushing updated index to MongoDB Cloud...")
            data = {
                "stored_items": search_engine.stored_items,
                "keyword_index": search_engine.keyword_index
            }
            mongodb.save_search_index(data)
            print("Successfully synced to MongoDB!")
    else:
        print("Could not find a 1434 template item to copy.")

if __name__ == "__main__":
    main()
