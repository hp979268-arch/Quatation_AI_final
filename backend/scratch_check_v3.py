import json
import os

with open('search_index_v2.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

v3_count = 0
revertible_items = []
small_originals = []
no_originals = []

for item in db['stored_items']:
    code = item.get('search_code', '')
    if item.get('images'):
        current_img = item['images'][0]
        if '_v3.png' in current_img:
            v3_count += 1
            
            # Possible original filenames
            # K-27484IN-4-CP.png
            # K-27484IN-4 CP.png
            
            orig_name_1 = current_img.replace('_v3.png', '.png')
            orig_name_2 = current_img.replace('_v3.png', '').replace('-', ' ') + '.png' # Rough approximation
            
            orig_path = '.' + orig_name_1
            
            if os.path.exists(orig_path):
                size = os.path.getsize(orig_path)
                if size > 5000:
                    revertible_items.append((code, orig_path, size))
                else:
                    small_originals.append((code, orig_path, size))
            else:
                # Try finding any .png that matches the start of the code
                # For simplicity, just say no exact match
                no_originals.append(code)

print(f"Total items using _v3.png: {v3_count}")
print(f"Items that have a valid original .png (>5KB) to revert to: {len(revertible_items)}")
print(f"Items with small original .png (<5KB): {len(small_originals)}")
print(f"Items with no exact original .png: {len(no_originals)}")

# Print a sample of revertible items
print("\nSample of revertible items:")
for c, p, s in revertible_items[:20]:
    print(f"  {c} -> {s} bytes")
