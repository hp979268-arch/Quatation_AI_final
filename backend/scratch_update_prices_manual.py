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
    
    fixed = 0
    for item in items:
        search_code = item.get("search_code", "")
        name = item.get("name", "")
        text = item.get("text", "")
        
        # 1438
        if "1438" in search_code.split() or "1438" in name.split() or search_code.startswith("1438"):
            print(f"Updating 1438: {name} (Old price: {item.get('price')})")
            item['price'] = "155000"
            item['text'] = update_mrp_in_text(text, "155000")
            fixed += 1
            
        # 1434-1200mm
        elif "1434" in search_code and "1200" in search_code:
            print(f"Updating 1434-1200mm: {name} (Old price: {item.get('price')})")
            item['price'] = "18250"
            item['text'] = update_mrp_in_text(text, "18250")
            fixed += 1
            
        # 1794 SM
        elif "1794" in search_code and "SM" in search_code:
            print(f"Updating 1794 SM: {name} (Old price: {item.get('price')})")
            item['price'] = "29500"
            item['text'] = update_mrp_in_text(text, "29500")
            fixed += 1
            
    if fixed > 0:
        print(f"Updated {fixed} items. Saving to MongoDB...")
        if mongodb.is_enabled():
            data = {
                "stored_items": items,
                "keyword_index": search_engine.keyword_index
            }
            mongodb.save_search_index(data)
            print("Successfully synced to MongoDB!")
    else:
        print("No items found to update.")

if __name__ == "__main__":
    main()
