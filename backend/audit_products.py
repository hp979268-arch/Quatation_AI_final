import json
import os

INDEX_FILE = "search_index_v2.json"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("stored_items", [])
print(f"Total items: {len(items)}")

# --- Counters ---
no_image = []
broken_image_path = []
no_price = []
zero_price = []
no_name = []
no_sku = []
duplicate_sku = {}
brand_counts = {}
price_suspicious = []  # price too low or too high

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

for idx, item in enumerate(items):
    brand = item.get("brand", "Unknown")
    brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    # Check name
    name = (item.get("display_name") or item.get("name") or "").strip()
    if not name:
        no_name.append(idx)
    
    # Check SKU
    sku = (item.get("sku") or item.get("search_code") or item.get("base_code") or "").strip()
    if not sku:
        no_sku.append(idx)
    else:
        if sku in duplicate_sku:
            duplicate_sku[sku].append(idx)
        else:
            duplicate_sku[sku] = [idx]
    
    # Check images
    images = item.get("images", [])
    img = images[0] if images else ""
    if not img:
        no_image.append((idx, name or f"Item#{idx}", brand))
    elif "Image_Not_Found" in img or "Image not Found" in img:
        broken_image_path.append((idx, name or f"Item#{idx}", brand, img))
    else:
        # Check if file exists on disk
        if img.startswith("/static/"):
            full_path = os.path.join(os.path.dirname(__file__), img.lstrip("/"))
            if not os.path.exists(full_path):
                broken_image_path.append((idx, name or f"Item#{idx}", brand, img))
    
    # Check price
    price_raw = item.get("price", "")
    try:
        price = float(str(price_raw).replace(",", "")) if price_raw else 0
    except:
        price = 0
    
    if not price_raw or price_raw == "":
        no_price.append((idx, name or f"Item#{idx}", brand))
    elif price == 0:
        zero_price.append((idx, name or f"Item#{idx}", brand))
    elif price < 50:
        price_suspicious.append((idx, name or f"Item#{idx}", brand, price, "TOO LOW (<50)"))
    elif price > 500000:
        price_suspicious.append((idx, name or f"Item#{idx}", brand, price, "TOO HIGH (>5L)"))

# --- Report ---
print("\n" + "="*60)
print("PRODUCT AUDIT REPORT")
print("="*60)

print(f"\n[BRANDS] Brand Distribution:")
for b, c in sorted(brand_counts.items(), key=lambda x: -x[1]):
    print(f"   {b}: {c} items")

print(f"\n[ERROR] Items with NO NAME: {len(no_name)}")
for idx in no_name[:10]:
    print(f"   Index {idx}: {json.dumps(items[idx], ensure_ascii=False)[:200]}")

print(f"\n[ERROR] Items with NO SKU/Code: {len(no_sku)}")
for idx in no_sku[:10]:
    it = items[idx]
    print(f"   Index {idx}: name='{it.get('name','')[:50]}' brand={it.get('brand','')}")

print(f"\n[IMAGE] Items with NO IMAGE: {len(no_image)}")
for idx, name, brand in no_image[:15]:
    print(f"   Index {idx}: {name[:50]} [{brand}]")

print(f"\n[IMAGE] Items with BROKEN/MISSING image file: {len(broken_image_path)}")
for idx, name, brand, img in broken_image_path[:15]:
    print(f"   Index {idx}: {name[:50]} [{brand}] -> {img[:60]}")

print(f"\n[PRICE] Items with NO PRICE: {len(no_price)}")
for idx, name, brand in no_price[:15]:
    print(f"   Index {idx}: {name[:50]} [{brand}]")

print(f"\n[PRICE] Items with ZERO PRICE: {len(zero_price)}")
for idx, name, brand in zero_price[:15]:
    print(f"   Index {idx}: {name[:50]} [{brand}]")

print(f"\n[WARN] Items with SUSPICIOUS PRICE: {len(price_suspicious)}")
for idx, name, brand, price, reason in price_suspicious[:20]:
    print(f"   Index {idx}: {name[:50]} [{brand}] -> Rs.{price} ({reason})")

# Duplicates
dupes = {k: v for k, v in duplicate_sku.items() if len(v) > 1}
print(f"\n[DUPE] Duplicate SKUs: {len(dupes)}")
for sku, indices in list(dupes.items())[:15]:
    names = [items[i].get("name","")[:30] for i in indices]
    print(f"   SKU '{sku}': indices {indices} -> {names}")

print("\n" + "="*60)
print("AUDIT COMPLETE")
print("="*60)
