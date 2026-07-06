"""
Fix 30006/30007 image URLs to use existing combined image files.
Also add Gold (G) variant which was missing.
"""
import json

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
items = data["stored_items"]

# Mapping: variant_code -> existing image filename
VARIANT_IMG = {
    "CP":  "30006-30007 CP.png",
    "G":   "30006-30007 G.png",
    "BRG": "30006-30007 BRG.png",
    "BG":  "30006-30007 BG.png",
    "GG":  "30006-30007 GG.png",
    "MB":  "30006-30007 MB.png",
    "RG":  "30006-30007 RG.png",
}

fixed = 0
for item in items:
    bc = item.get("base_code","")
    vc = item.get("variant_code","").upper()
    if bc in ("30006","30007") and vc in VARIANT_IMG:
        fname = VARIANT_IMG[vc]
        new_url = f"/static/images/Aquant/{fname}?v=8"
        item["images"] = [new_url]
        print(f"  [FIX] {item.get('search_code')} -> {fname}")
        fixed += 1

# Also add missing Gold (G) variants
def find_item(base_code, variant_code):
    for i in items:
        if i.get("base_code","") == base_code and i.get("variant_code","").upper() == variant_code.upper():
            return i
    return None

# 30006 G
if not find_item("30006","G"):
    items.append({
        "text": "30006 G - Extendible Shower Hose (SS) 1.0 mtr Gold\nExtendible Shower Hose Gold",
        "name": "30006 G - Extendible Shower Hose (SS) 1.0 mtr",
        "price": "1700",
        "page": 20,
        "source": "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": ["/static/images/Aquant/30006-30007 G.png?v=8"],
        "brand": "Aquant",
        "category": "FAUCETS & SHOWERING SYSTEMS IN SPECIAL FINISHES",
        "base_code": "30006",
        "variant_code": "G",
        "search_code": "30006 G",
        "finish_label": "Gold"
    })
    print("  [ADD] 30006 G @ 1700")

# 30007 G
if not find_item("30007","G"):
    items.append({
        "text": "30007 G - Extendible Shower Hose (SS) 1.5 mtr Gold\nExtendible Shower Hose Gold",
        "name": "30007 G - Extendible Shower Hose (SS) 1.5 mtr",
        "price": "1850",
        "page": 20,
        "source": "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": ["/static/images/Aquant/30006-30007 G.png?v=8"],
        "brand": "Aquant",
        "category": "FAUCETS & SHOWERING SYSTEMS IN SPECIAL FINISHES",
        "base_code": "30007",
        "variant_code": "G",
        "search_code": "30007 G",
        "finish_label": "Gold"
    })
    print("  [ADD] 30007 G @ 1850")

data["stored_items"] = items
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"\nFixed {fixed} image URLs. Total items: {len(items)}")
print("Saved.")
