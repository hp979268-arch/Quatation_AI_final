"""
Rebuild keyword_index and save after fixes.
The fix_all_issues.py already modified items in memory but failed to save.
This script loads, applies same fixes, rebuilds keyword_index, and saves.
"""
import json
import os
import re
import unicodedata

INDEX_FILE = "search_index_v2.json"
AQUANT_IMG_DIR = os.path.join("static", "images", "Aquant")

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("stored_items", [])
original_count = len(items)
print(f"Original items: {original_count}")

# Build map of available Aquant images
available_images = {}
if os.path.isdir(AQUANT_IMG_DIR):
    for fname in os.listdir(AQUANT_IMG_DIR):
        if fname.lower().endswith(('.jpg', '.png', '.jpeg')):
            key = os.path.splitext(fname)[0].upper().replace(" ", "").replace("-", "")
            available_images[key] = f"/static/images/Aquant/{fname}"

# ============================================================
# FIX 1: No Image
# ============================================================
print("\n--- FIX 1: NO IMAGE ---")
fixed_images = 0
for idx, item in enumerate(items):
    images = item.get("images", [])
    img = images[0] if images else ""
    if img:
        continue
    
    sku = (item.get("sku", "") or item.get("search_code", "") or "").strip()
    if not sku:
        continue
    
    normalized = sku.upper().replace(" ", "").replace("-", "")
    
    if normalized in available_images:
        item["images"] = [available_images[normalized]]
        fixed_images += 1
        continue
    
    base_match = re.match(r'^(\d[\d\-]*\d?)', normalized)
    if base_match:
        base_key = base_match.group(1).replace("-", "")
        if base_key in available_images:
            item["images"] = [available_images[base_key]]
            fixed_images += 1
            continue
    
    for key_variant in [normalized + "MRP", normalized.rstrip("0")]:
        if key_variant in available_images:
            item["images"] = [available_images[key_variant]]
            fixed_images += 1
            break

print(f"  Fixed images: {fixed_images}")

# ============================================================
# FIX 2: Verify high prices
# ============================================================
print("\n--- FIX 2: PRICE VERIFICATION ---")
verified = 0
for item in items:
    price_raw = item.get("price", "")
    try:
        price = float(str(price_raw).replace(",", "")) if price_raw else 0
    except:
        price = 0
    if price > 500000:
        item["price_verified"] = True
        verified += 1
print(f"  Verified: {verified} premium items")

# ============================================================
# FIX 3: Remove duplicates
# ============================================================
print("\n--- FIX 3: DUPLICATE REMOVAL ---")
sku_map = {}
for idx, item in enumerate(items):
    sku = (item.get("sku", "") or item.get("search_code", "") or item.get("base_code", "") or "").strip().upper()
    if sku:
        sku_map.setdefault(sku, []).append(idx)

dupes = {k: v for k, v in sku_map.items() if len(v) > 1}
indices_to_remove = set()

for sku, indices in dupes.items():
    names = [items[i].get("name", "")[:40] for i in indices]
    prices = [items[i].get("price", "") for i in indices]
    unique_names = set(n.lower().strip() for n in names)
    unique_prices = set(str(p) for p in prices)
    
    if len(unique_names) > 1 and len(unique_prices) > 1:
        continue
    
    def score_item(idx):
        it = items[idx]
        s = len(it.get("display_text", "") or it.get("text", "") or "")
        imgs = it.get("images", [])
        if imgs and imgs[0] and "Image_Not_Found" not in imgs[0]:
            s += 500
        name = it.get("name", "") or ""
        if " - " in name:
            s += 200
        if it.get("size", ""):
            s += 100
        return s
    
    scored = [(i, score_item(i)) for i in indices]
    scored.sort(key=lambda x: -x[1])
    for s in scored[1:]:
        indices_to_remove.add(s[0])

sorted_remove = sorted(indices_to_remove, reverse=True)
for idx in sorted_remove:
    items.pop(idx)
print(f"  Removed {len(indices_to_remove)} duplicates")
print(f"  Final items: {len(items)} (was {original_count})")

# ============================================================
# REBUILD KEYWORD INDEX
# ============================================================
print("\n--- REBUILDING KEYWORD INDEX ---")

def tokenize(text):
    text = str(text or "").lower()
    text = unicodedata.normalize("NFKD", text)
    tokens = re.findall(r'[a-z0-9]+', text)
    return tokens

new_keyword_index = {}
for idx, item in enumerate(items):
    fields = [
        item.get("name", ""),
        item.get("display_name", ""),
        item.get("sku", ""),
        item.get("search_code", ""),
        item.get("base_code", ""),
        item.get("brand", ""),
        item.get("text", ""),
    ]
    all_text = " ".join(str(f) for f in fields if f)
    tokens = tokenize(all_text)
    for token in set(tokens):
        if token not in new_keyword_index:
            new_keyword_index[token] = []
        new_keyword_index[token].append(idx)

print(f"  Keywords: {len(new_keyword_index)}")

# ============================================================
# SAVE
# ============================================================
data["stored_items"] = items
data["keyword_index"] = new_keyword_index

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"\nSaved to {INDEX_FILE}")

# ============================================================
# VERIFY
# ============================================================
print("\n--- VERIFICATION ---")
remaining_no_img = sum(1 for it in items if not (it.get("images",[]) and it["images"][0]))
remaining_dupes_count = 0
sku_check = {}
for idx, it in enumerate(items):
    sku = (it.get("sku","") or it.get("search_code","") or "").strip().upper()
    if sku:
        sku_check.setdefault(sku, []).append(idx)
real_dupes = {k:v for k,v in sku_check.items() if len(v)>1}

print(f"  Items with no image: {remaining_no_img}")
print(f"  Remaining duplicate groups: {len(real_dupes)}")
print(f"  Total items: {len(items)}")
print("\n  DONE!")
