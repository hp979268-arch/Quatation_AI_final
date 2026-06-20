import json
import os
import re

INDEX_FILE = "search_index_v2.json"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("stored_items", [])

# ============================================================
# 1. DETAILED: No Image items (53)
# ============================================================
print("="*70)
print("1. NO IMAGE ITEMS - DETAILED")
print("="*70)
no_image_items = []
for idx, item in enumerate(items):
    images = item.get("images", [])
    img = images[0] if images else ""
    if not img:
        no_image_items.append(idx)

print(f"Total: {len(no_image_items)}")
for idx in no_image_items:
    it = items[idx]
    sku = it.get("sku","") or it.get("search_code","") or it.get("base_code","")
    name = it.get("display_name","") or it.get("name","")
    price = it.get("price","")
    brand = it.get("brand","")
    print(f"  [{idx}] SKU={sku} | name={name[:60]} | price={price} | brand={brand}")
    print(f"         images={it.get('images',[])} | keys={list(it.keys())}")

# ============================================================
# 2. DETAILED: Suspicious Price items (>5L)
# ============================================================
print("\n" + "="*70)
print("2. SUSPICIOUS PRICE (>5L) - DETAILED")
print("="*70)
for idx, item in enumerate(items):
    price_raw = item.get("price", "")
    try:
        price = float(str(price_raw).replace(",", "")) if price_raw else 0
    except:
        price = 0
    if price > 500000:
        sku = item.get("sku","") or item.get("search_code","") or item.get("base_code","")
        name = item.get("display_name","") or item.get("name","")
        text = (item.get("display_text","") or item.get("text",""))[:200]
        print(f"  [{idx}] SKU={sku} | price={price} | name={name[:60]}")
        print(f"         text_excerpt: {text[:120]}")
        print()

# ============================================================
# 3. DETAILED: Duplicate SKUs
# ============================================================
print("\n" + "="*70)
print("3. DUPLICATE SKUs - DETAILED")
print("="*70)
sku_map = {}
for idx, item in enumerate(items):
    sku = (item.get("sku","") or item.get("search_code","") or item.get("base_code","") or "").strip()
    if sku:
        sku_map.setdefault(sku, []).append(idx)

dupes = {k: v for k, v in sku_map.items() if len(v) > 1}
print(f"Total duplicate groups: {len(dupes)}")
for sku, indices in dupes.items():
    print(f"\n  SKU: '{sku}' ({len(indices)} entries)")
    for idx in indices:
        it = items[idx]
        name = it.get("display_name","") or it.get("name","")
        price = it.get("price","")
        imgs = it.get("images",[])
        has_img = bool(imgs and imgs[0] and "Image_Not_Found" not in imgs[0])
        text_len = len(it.get("display_text","") or it.get("text","") or "")
        size = it.get("size","")
        print(f"    [{idx}] name={name[:50]} | price={price} | has_img={has_img} | text_len={text_len} | size={size}")
