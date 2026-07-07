import sys
import os
import json
import re
import urllib.request

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
    
    rules = {
        "1311": {"suffixes": ["GG", "MB", "RG"], "price": "9100"},
        "1312": {"suffixes": ["GG", "MB", "RG"], "price": "10250"},
        "1316": {"suffixes": ["GG", "MB", "RG"], "price": "12950"},
        "1442": {"suffixes": ["GG", "MB", "RG"], "price": "4750"},
        "1125": {"suffixes": ["GG"], "price": "4400"},
        "2727": {"suffixes": ["BRG", "BG", "GG", "MB", "RG"], "price": "2650"},
        "2746": {"suffixes": ["GG", "MB"], "price": "3950"}
    }
    
    fixed = 0
    for item in items:
        search_code = item.get("search_code", "")
        name = item.get("name", "")
        
        for rule_base, rule_data in rules.items():
            if rule_base in search_code or rule_base in name:
                for suffix in rule_data["suffixes"]:
                    # Match pattern: base_code followed by optional space/dash, then the EXACT suffix.
                    # e.g., "1311 GG", "1311-GG", "1311GG"
                    pattern = rf"{rule_base}[-\s]*{suffix}\b"
                    if re.search(pattern, search_code, re.IGNORECASE) or re.search(pattern, name, re.IGNORECASE):
                        old_price = item.get('price')
                        new_price = rule_data["price"]
                        
                        if old_price != new_price:
                            print(f"Updating {search_code} (Matched {rule_base} {suffix}): {old_price} -> {new_price}")
                            item['price'] = new_price
                            item['text'] = update_mrp_in_text(item.get('text', ''), new_price)
                            fixed += 1
                        break # Prevent multiple suffix matches on the same item
                        
    if fixed > 0:
        print(f"\nUpdated {fixed} items. Saving to MongoDB...")
        if mongodb.is_enabled():
            data = {
                "stored_items": items,
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
        print("No items found to update.")

if __name__ == "__main__":
    main()
