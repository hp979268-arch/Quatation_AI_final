"""
Fix remaining issues:
1. 2563 GG/MB/RG -> 36750
2. 2741 all non-CP -> 3000 (PDF pg48: non-CP MRP=3000)
3. 1424-200 non-CP -> 3300 (PDF pg40: 200mm Brass Ext Pipe MRP=3300)
4. Add 1419 RG variant
"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    d = json.load(f)
items = d["stored_items"]

def fix_price(base, variant, new_price):
    for item in items:
        if (item.get("base_code","").upper() == base.upper() and
            item.get("variant_code","").upper() == variant.upper()):
            old = item["price"]
            item["price"] = str(new_price)
            print(f"  [FIX] {item.get('search_code')} | {old} -> {new_price}")
            return True
    print(f"  [SKIP] {base} {variant} not found")
    return False

def exists(base, variant):
    return any(i.get("base_code","").upper()==base.upper() and
               i.get("variant_code","").upper()==variant.upper() for i in items)

print("=== FIX 1: 2563 GG/MB/RG -> 36750 ===")
fix_price("2563","GG", 36750)
fix_price("2563","MB", 36750)
fix_price("2563","RG", 36750)

print("\n=== FIX 2: 2741 all non-CP -> 3000 ===")
for vc in ["BRG","BG","GG","MB","RG"]:
    fix_price("2741", vc, 3000)

print("\n=== FIX 3: 1424-200 non-CP -> 3300 ===")
for vc in ["BRG","BG","GG","MB","RG"]:
    fix_price("1424-200", vc, 3300)

print("\n=== FIX 4: Add 1419 RG variant ===")
if not exists("1419","RG"):
    items.append({
        "text": "1419 RG - Brass Button Spout\nBrass Button Spout Rose Gold",
        "name": "1419 RG - Brass Button Spout",
        "price": "8250",
        "page": 31,
        "source": "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": ["/static/images/Aquant/1419.png?v=8"],
        "brand": "Aquant",
        "category": "FAUCETS & SPOUTS IN SPECIAL FINISHES",
        "base_code": "1419",
        "variant_code": "RG",
        "search_code": "1419 RG",
        "finish_label": "Rose Gold"
    })
    print("  [ADD] 1419 RG @ 8250")

    # Add to keyword index
    ki = d.get("keyword_index", {})
    pos = len(items) - 1
    for k in ["1419","1419rg","spout","buttonspout"]:
        if k not in ki: ki[k] = []
        if pos not in ki[k]: ki[k].append(pos)
    d["keyword_index"] = ki
else:
    print("  [SKIP] 1419 RG already exists")

print("\n=== SAVING ===")
d["stored_items"] = items
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)
print(f"  Saved. Total items: {len(items)}")

print("\n=== VERIFY ===")
def show(base):
    vs = {i.get("variant_code",""):i.get("price") for i in items
          if i.get("base_code","").upper()==base.upper()}
    print(f"  {base}: {vs}")

show("2563")
show("2741")
show("1424-200")
show("1419")
