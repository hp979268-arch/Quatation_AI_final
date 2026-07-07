import os
import sys
import json
import argparse
import subprocess

INDEX_PATH = "search_index_v2.json"

def main():
    parser = argparse.ArgumentParser(description="Find a product and update its price in Shreeji Ceramica Quotation AI catalog.")
    parser.add_argument("--query", help="Search query (e.g., product code, search_code, name)")
    parser.add_argument("--price", help="New price to set")
    parser.add_argument("--push", action="store_true", help="Push changes to MongoDB instantly")
    
    args = parser.parse_args()
    
    if not os.path.exists(INDEX_PATH):
        print(f"ERROR: {INDEX_PATH} not found in the current directory.")
        return
        
    print(f"Loading {INDEX_PATH}...")
    with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        
    items = data.get("stored_items", [])
    print(f"Loaded {len(items)} products.")
    
    # Get query
    query = args.query
    if not query:
        query = input("Enter product code, search_code, or name to find: ").strip()
        if not query:
            print("Cancelled.")
            return
            
    query_lower = query.lower()
    matches = []
    for idx, item in enumerate(items):
        code = str(item.get("base_code") or "").lower()
        search_code = str(item.get("search_code") or "").lower()
        name = str(item.get("name") or "").lower()
        text = str(item.get("text") or "").lower()
        
        if query_lower in code or query_lower in search_code or query_lower in name or query_lower in text:
            matches.append((idx, item))
            
    if not matches:
        print("No matching products found.")
        return
        
    print(f"\nFound {len(matches)} matching product(s):")
    for i, (idx, item) in enumerate(matches):
        print(f"[{i}] {item.get('brand')} | Code: {item.get('search_code') or item.get('base_code')} | Name: {item.get('name')} | Current Price: {item.get('price')}")
        
    # Choose item
    selected_idx = None
    if len(matches) == 1:
        selected_idx = 0
        print(f"\nOnly 1 match found. Selected: {matches[0][1].get('name')}")
    else:
        choice = input(f"\nSelect product index (0 to {len(matches)-1}): ").strip()
        try:
            selected_idx = int(choice)
            if selected_idx < 0 or selected_idx >= len(matches):
                print("Invalid choice.")
                return
        except ValueError:
            print("Invalid input.")
            return
            
    original_idx, target_item = matches[selected_idx]
    
    # Get price
    new_price = args.price
    if not new_price:
        new_price = input(f"Enter new price for {target_item.get('name')} (Current: {target_item.get('price')}): ").strip()
        if not new_price:
            print("Cancelled.")
            return
            
    old_price = target_item.get('price')
    target_item['price'] = new_price
    if 'mrp' in target_item:
        target_item['mrp'] = new_price
        
    if target_item.get('text') and old_price:
        target_item['text'] = target_item['text'].replace(old_price, new_price)
        
    # Save index
    print("\nSaving updated index...")
    # Bump version to bust cache
    if 'version' in data:
        import time
        data['version'] = str(int(time.time()))
        
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"SUCCESS: Updated {target_item.get('name')} price to {new_price} in {INDEX_PATH}!")
    
    # Push to MongoDB
    push = args.push
    if not push:
        push_choice = input("Do you want to push this update to MongoDB Cloud now? (y/n): ").strip().lower()
        push = push_choice in ['y', 'yes']
        
    if push:
        print("\nRunning direct_mongo_push.py to update MongoDB...")
        try:
            res = subprocess.run(["python", "direct_mongo_push.py"], capture_output=True, text=True)
            print(res.stdout)
            if res.stderr:
                print("Error output:", res.stderr)
        except Exception as e:
            print(f"Failed to execute direct_mongo_push.py: {e}")
            
if __name__ == "__main__":
    main()
