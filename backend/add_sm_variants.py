import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    d = json.load(f)
items = d["stored_items"]
ki = d.get("keyword_index", {})

def exists(base, vc):
    return any(i.get("base_code","") == base and i.get("variant_code","").upper() == vc.upper() for i in items)

def add_sm(base_code, size, description):
    if exists(base_code, "SM"):
        print(f"  [SKIP] {base_code} SM already exists")
        return
    sc = f"{base_code} SM"
    new_item = {
        "text": f"{sc} - {description} Statuario Matt Finish\n{description}",
        "name": f"{sc} - {description}",
        "price": "14000",
        "page": 85,
        "source": "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": [f"/static/images/Aquant/{base_code}SM.png?v=8"],
        "brand": "Aquant",
        "category": "CERAMIC WASH BASINS",
        "base_code": base_code,
        "variant_code": "SM",
        "search_code": sc,
        "finish_label": "Statuario Matt",
        "size": size
    }
    items.append(new_item)
    pos = len(items) - 1
    for k in [base_code, base_code+"sm", sc.lower().replace(" ",""), "statuario", "statuariomatt", "washbasin", "basin"]:
        if k not in ki: ki[k] = []
        if pos not in ki[k]: ki[k].append(pos)
    print(f"  [ADD] {sc} @ Rs.14000 | {size}")

add_sm("1902", "550 x 400 x 140 mm", "Table Mounted Wash Basin")
add_sm("1936", "525 x 410 x 160 mm", "Table Mounted Wash Basin")

d["stored_items"] = items
d["keyword_index"] = ki
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)

print(f"\nTotal items: {len(items)}")
print("Saved.")
