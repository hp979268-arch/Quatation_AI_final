"""
Complete fix script for all reported issues.
1. Price fixes (34+ items)
2. Add missing products
3. Save updated index
READ: Verify output then run mongo_push separately.
"""
import json, sys, io, copy, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data["stored_items"]
keyword_index = data.get("keyword_index", {})

# Track changes
fixed = []
added = []

def find_item(base_code, variant_code=""):
    for i, item in enumerate(items):
        if (item.get("base_code","").upper() == base_code.upper() and
            item.get("variant_code","").upper() == variant_code.upper()):
            return i, item
    return None, None

def fix_price(base_code, variant_code, new_price, note=""):
    idx, item = find_item(base_code, variant_code)
    if item:
        old = item["price"]
        item["price"] = str(new_price)
        sc = item.get("search_code", base_code + " " + variant_code)
        fixed.append(f"FIXED: {sc} | {old} -> {new_price} | {note}")
        print(f"  [FIX] {sc}: {old} -> {new_price}")
    else:
        print(f"  [SKIP] {base_code} {variant_code} not found")

def fix_all_variants(base_code, new_price, exclude=None, note=""):
    exclude = exclude or []
    for item in items:
        if item.get("base_code","").upper() == base_code.upper():
            vc = item.get("variant_code","").upper()
            if vc not in [e.upper() for e in exclude]:
                old = item["price"]
                item["price"] = str(new_price)
                sc = item.get("search_code","?")
                fixed.append(f"FIXED: {sc} | {old} -> {new_price} | {note}")
                print(f"  [FIX] {sc}: {old} -> {new_price}")

# ============================================================
# PRICE FIXES
# ============================================================
print("\n=== PRICE FIXES ===\n")

# PG-91: 1501 Concealed Pneumatic Cistern Full Frame
fix_price("1501", "", 20990, "pg91 Full Frame cistern")

# PG-86/90: 1506 Smart Toilet Cistern
fix_price("1506", "", 27500, "pg86 Smart toilet cistern")

# PG-91: 1507 non-BSS flush plates
fix_price("1507", "GG", 17750, "pg91 flush plate")
fix_price("1507", "BG", 17750, "pg91 flush plate")
fix_price("1507", "MB", 17750, "pg91 flush plate")
fix_price("1507", "BRG", 17750, "pg91 flush plate")

# PG-85: 1947 Under Counter Basin 1000mm
fix_price("1947", "", 43500, "pg85 under counter basin")

# PG-66/77: 9057-Konig Stone Basin
fix_price("9057", "", 99000, "pg66 Konig stone basin")

# PG-56: Shower Panels
fix_price("1258", "", 41000, "pg56 Revive shower panel")
fix_price("1257", "", 38500, "pg56 Retro shower panel")
fix_price("1256", "", 70000, "pg56 Eden shower panel")
fix_price("1245", "", 74500, "pg56 Divine shower panel")

# PG-57: 1439-Fleur Shower Column
fix_price("1439", "", 57500, "pg57 Fleur shower column")

# PG-61: 28088 ABS Wall Hook
fix_price("28088", "", 120, "pg61 ABS wall hook")

# PG-54: Hand Showers
fix_price("28197", "", 700, "pg54 ABS head shower 110mm")
fix_price("28198", "", 700, "pg54 ABS hand shower 100mm")

# PG-63: Connectors & accessories
fix_price("1151", "", 220, "pg63 hose 300mm")
fix_price("1152", "", 240, "pg63 hose 450mm")
fix_price("1153", "", 260, "pg63 hose 600mm")
fix_price("1460", "", 500, "pg63 WC connector 125mm")
fix_price("1462", "", 550, "pg63 WC connector 250mm")
fix_price("1487", "", 500, "pg63 WC offset connector")
fix_price("1461", "", 80, "pg63 WC rubber washer")
fix_price("1010", "", 950, "pg63 liquid cleaner")

# PG-59: Floor Drains
fix_price("1436", "BRG", 4750, "pg59 shower drainer BRG")
fix_price("1436", "BG", 4750, "pg59 shower drainer BG")
fix_price("1436", "GG", 4750, "pg59 shower drainer GG")
fix_price("1436", "MB", 4750, "pg59 shower drainer MB")

fix_price("1318", "BRG", 4250, "pg59 tile insert 100mm BRG")
fix_price("1318", "BG", 4250, "pg59 tile insert 100mm BG")
fix_price("1318", "GG", 4250, "pg59 tile insert 100mm GG")
fix_price("1318", "MB", 4250, "pg59 tile insert 100mm MB")

fix_price("1319", "BRG", 7000, "pg59 tile insert 150mm BRG")
fix_price("1319", "BG", 7000, "pg59 tile insert 150mm BG")
fix_price("1319", "GG", 7000, "pg59 tile insert 150mm GG")
fix_price("1319", "MB", 7000, "pg59 tile insert 150mm MB")

# PG-58: Shower Channel Base (BSCH)
fix_price("60080", "BS CH", 4400, "pg58 shower channel 600mm")
fix_price("750080", "BS CH", 5000, "pg58 shower channel 750mm")
fix_price("90080", "BS CH", 6100, "pg58 shower channel 900mm")

# PG-44: Accessories
fix_price("7011", "BRG", 35000, "pg44 SS niche BRG")
fix_price("7011", "BG", 35000, "pg44 SS niche BG")
fix_price("7011", "GG", 35000, "pg44 SS niche GG")
fix_price("7011", "MB", 35000, "pg44 SS niche MB")

fix_price("2650", "BRG", 7250, "pg44 dustbin BRG")
fix_price("2650", "BG", 7250, "pg44 dustbin BG")
fix_price("2650", "GG", 7250, "pg44 dustbin GG")
fix_price("2650", "MB", 7250, "pg44 dustbin MB")

# PG-48: Tower Bar & Robe Hook
fix_price("2750", "BRG", 7250, "pg48 double tower bar")
fix_price("2750", "BG", 7250, "pg48 double tower bar")
fix_price("2750", "GG", 7250, "pg48 double tower bar")
fix_price("2750", "MB", 7250, "pg48 double tower bar")

# PG-47: Accessories Quadra
fix_price("2728", "BRG", 5500, "pg47 toilet brush holder")
fix_price("2728", "BG", 5500, "pg47 toilet brush holder")
fix_price("2728", "GG", 5500, "pg47 toilet brush holder")
fix_price("2728", "MB", 5500, "pg47 toilet brush holder")
fix_price("2728", "RG", 5500, "pg47 toilet brush holder")

fix_price("2726", "BRG", 3550, "pg47 tumbler holder")
fix_price("2726", "BG", 3550, "pg47 tumbler holder")
fix_price("2726", "GG", 3550, "pg47 tumbler holder")
fix_price("2726", "MB", 3550, "pg47 tumbler holder")
fix_price("2726", "RG", 3550, "pg47 tumbler holder")

fix_price("2729", "BRG", 2950, "pg47 toilet roll holder")
fix_price("2729", "BG", 2950, "pg47 toilet roll holder")
fix_price("2729", "GG", 2950, "pg47 toilet roll holder")
fix_price("2729", "MB", 2950, "pg47 toilet roll holder")
fix_price("2729", "RG", 2950, "pg47 toilet roll holder")

# PG-46: Robe Hook
fix_price("2721", "BRG", 1950, "pg46 robe hook")
fix_price("2721", "BG", 1950, "pg46 robe hook")
fix_price("2721", "GG", 1950, "pg46 robe hook")
fix_price("2721", "MB", 1950, "pg46 robe hook")
fix_price("2721", "RG", 1950, "pg46 robe hook")

# PG-45: Brass Mirror with LED
fix_price("1472", "BRG", 28250, "pg45 brass mirror LED")
fix_price("1472", "BG", 28250, "pg45 brass mirror LED")
fix_price("1472", "GG", 28250, "pg45 brass mirror LED")
fix_price("1472", "MB", 28250, "pg45 brass mirror LED")
fix_price("1472", "RG", 28250, "pg45 brass mirror LED")

# PG-29/30: Thermostatic variants - BRG/BG different price
fix_price("2106", "BRG", 65000, "pg30 4-outlet diverter BRG")
fix_price("2106", "BG", 65000, "pg30 4-outlet diverter BG")

fix_price("2104", "BRG", 59000, "pg30 3-outlet diverter BRG")
fix_price("2104", "BG", 59000, "pg30 3-outlet diverter BG")

fix_price("2122", "BRG", 115000, "pg28 4-outlet thermostat BRG")
fix_price("2122", "BG", 115000, "pg28 4-outlet thermostat BG")
fix_price("2122", "GG", 115000, "pg28 4-outlet thermostat GG")
fix_price("2122", "MB", 115000, "pg28 4-outlet thermostat MB")
fix_price("2122", "RG", 115000, "pg28 4-outlet thermostat RG")

fix_price("2114", "GG", 138500, "pg29 4-outlet switch thermostat GG")
fix_price("2114", "MB", 138500, "pg29 4-outlet switch thermostat MB")
fix_price("2114", "RG", 138500, "pg29 4-outlet switch thermostat RG")

# PG-24: 2563 BRG/BG (PDF says 36,750 for non-CP, but GG/MB/RG = 31,500)
# PDF pg24: non-CP MRP = 36,750, CP = 27,250 -- index BRG/BG already 36,750 OK
# But user says mismatch - leave as is, verified OK

# PG-45: 1472 name fix (BG/GG/MB/RG show wrong name)
for item in items:
    if item.get("base_code","") == "1472" and item.get("variant_code","") in ["BG","GG","MB","RG"]:
        item["name"] = item["name"].replace("Brass Mirror With Dual LED Lig", "1472 " + item.get("variant_code","") + " - Brass Mirror With Dual LED Lights")
        item["name"] = "1472 " + item.get("variant_code","") + " - Brass Mirror With Dual LED Lights"

print(f"\n  Total price fixes: {len(fixed)}")

# ============================================================
# ADD MISSING PRODUCTS
# ============================================================
print("\n=== ADDING MISSING PRODUCTS ===\n")

def make_keyword_entries(item):
    """Add item to keyword index."""
    sc = item.get("search_code","").lower().replace(" ","")
    bc = item.get("base_code","").lower()
    name_words = item.get("name","").lower().replace("-","").split()
    keys = set([sc, bc, sc+item.get("base_code","").lower()])
    for w in name_words:
        if len(w) > 2:
            keys.add(w)
    # find item position
    pos = len(items) - 1
    for k in keys:
        if k:
            if k not in keyword_index:
                keyword_index[k] = []
            if pos not in keyword_index[k]:
                keyword_index[k].append(pos)

def add_item(base_code, variant_code, name, price, category, description,
             page, images=None, finish_label=""):
    search_code = (base_code + " " + variant_code).strip()
    # Check not duplicate
    idx, existing = find_item(base_code, variant_code)
    if existing:
        print(f"  [SKIP] {search_code} already exists")
        return
    new_item = {
        "text": f"{search_code} - {description}\n{description}",
        "name": f"{search_code} - {description}",
        "price": str(price),
        "page": page,
        "source": "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": images or [],
        "brand": "Aquant",
        "category": category,
        "base_code": base_code,
        "variant_code": variant_code,
        "search_code": search_code,
        "finish_label": finish_label
    }
    items.append(new_item)
    make_keyword_entries(new_item)
    added.append(f"ADDED: {search_code} @ {price}")
    print(f"  [ADD] {search_code} @ Rs.{price} | {description}")

# ---- 30006 / 30007 (Extendible Shower Hose SS) ----
# 30006 = 1.0m, 30007 = 1.5m
# CP prices: 30006=575, 30007=690
# Special finish (Gold/BRG/BG/GG/MB/RG): 30006=1700, 30007=1850

hose_cat = "ALLIED PRODUCTS IN SPECIAL FINISHES"
hose_img_30006 = ["/static/images/Aquant/30006.png?v=8"]
hose_img_30007 = ["/static/images/Aquant/30007.png?v=8"]

add_item("30006", "CP", "Extendible Shower Hose (SS) 1.0m", 575, hose_cat,
         "Extendible Shower Hose (SS) 1.0 mtr", 43, hose_img_30006, "Chrome Plated")
add_item("30007", "CP", "Extendible Shower Hose (SS) 1.5m", 690, hose_cat,
         "Extendible Shower Hose (SS) 1.5 mtr", 43, hose_img_30007, "Chrome Plated")

for vc, fl in [("BRG","Brushed Rose Gold"),("BG","Brushed Gold"),
               ("GG","Graphite Grey"),("MB","Matt Black"),("RG","Rose Gold")]:
    add_item("30006", vc, f"Extendible Shower Hose (SS) 1.0m", 1700, hose_cat,
             "Extendible Shower Hose (SS) 1.0 mtr", 20, hose_img_30006, fl)
    add_item("30007", vc, f"Extendible Shower Hose (SS) 1.5m", 1850, hose_cat,
             "Extendible Shower Hose (SS) 1.5 mtr", 20, hose_img_30007, fl)

# ---- 1320-750 (Tile Insert Channel 750mm) ----
drain_cat = "FLOOR DRAINS IN SPECIAL FINISHES"
img_1320 = ["/static/images/Aquant/1320.png?v=8"]
for vc, fl in [("BRG","Brushed Rose Gold"),("BG","Brushed Gold"),
               ("GG","Graphite Grey"),("MB","Matt Black")]:
    add_item("1320-750", vc, f"Tile Insert Channel Drainer 750mm", 17500, drain_cat,
             "Tile Insert Channel Drainer 750x85mm (304 SS, Side Outlet)", 59, img_1320, fl)

# ---- 1437-750 (Shower Channel Drainer 750mm) ----
img_1437 = ["/static/images/Aquant/1437.png?v=8"]
for vc, fl in [("BRG","Brushed Rose Gold"),("BG","Brushed Gold"),
               ("GG","Graphite Grey"),("MB","Matt Black")]:
    add_item("1437-750", vc, f"Shower Channel Drainer 750mm", 17750, drain_cat,
             "Shower Channel Drainer 750x100mm (304 SS, Side Outlet)", 59, img_1437, fl)

# ---- 1419 non-CP variants ----
spout_cat = "FAUCETS & SPOUTS IN SPECIAL FINISHES"
img_1419 = ["/static/images/Aquant/1419.png?v=8"]
for vc, fl in [("BRG","Brushed Rose Gold"),("BG","Brushed Gold"),
               ("GG","Graphite Grey"),("MB","Matt Black")]:
    add_item("1419", vc, f"Brass Button Spout", 8250, spout_cat,
             "Brass Button Spout", 31, img_1419, fl)

# ---- 1186 non-CP variants ----
hf_cat = "ALLIED PRODUCTS IN SPECIAL FINISHES"
img_1186 = ["/static/images/Aquant/1186.png?v=8"]
for vc, fl in [("BRG","Brushed Rose Gold"),("BG","Brushed Gold"),
               ("GG","Graphite Grey"),("MB","Matt Black"),("RG","Rose Gold")]:
    add_item("1186", vc, f"ABS Health Faucet Set With 1 mtr Hose", 5250, hf_cat,
             "ABS Health Faucet Set With 1 mtr Flexible Hose & Wall Hook", 43, img_1186, fl)

# ---- 1418 RG variant ----
img_1418 = ["/static/images/Aquant/1418.png?v=8"]
add_item("1418", "RG", "Brass Plain Spout", 8250, spout_cat,
         "Brass Plain Spout", 31, img_1418, "Rose Gold")

# ---- 2741 RG variant ----
acc_cat = "ACCESSORIES IN SPECIAL FINISHES"
img_2741 = ["/static/images/Aquant/2741.png?v=8"]
add_item("2741", "RG", "Robe Hook", 6000, acc_cat,
         "Robe Hook", 48, img_2741, "Rose Gold")

# ---- 1424-200 and 1424-500 extension pipes ----
pipe_cat = "FAUCETS IN SPECIAL FINISHES"
img_1424 = ["/static/images/Aquant/1424.png?v=8"]
add_item("1424-200", "CP", "Brass Extension Pipe 200mm", 2500, pipe_cat,
         "200mm Brass Extension Pipe", 40, img_1424, "Chrome Plated")
add_item("1424-500", "CP", "Brass Extension Pipe 500mm", 5500, pipe_cat,
         "500mm Brass Extension Pipe", 40, img_1424, "Chrome Plated")
for vc, fl in [("BRG","Brushed Rose Gold"),("BG","Brushed Gold"),
               ("GG","Graphite Grey"),("MB","Matt Black"),("RG","Rose Gold")]:
    add_item("1424-200", vc, "Brass Extension Pipe 200mm", 3300, pipe_cat,
             "200mm Brass Extension Pipe", 40, img_1424, fl)
    add_item("1424-500", vc, "Brass Extension Pipe 500mm", 7700, pipe_cat,
             "500mm Brass Extension Pipe", 40, img_1424, fl)

print(f"\n  Total products added: {len(added)}")

# ============================================================
# SAVE UPDATED INDEX
# ============================================================
print("\n=== SAVING INDEX ===")

# Backup first
import shutil
backup = INDEX_PATH.replace(".json", f"_backup_{int(time.time())}.json")
shutil.copy2(INDEX_PATH, backup)
print(f"  Backup: {backup}")

data["stored_items"] = items
data["keyword_index"] = keyword_index

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print(f"  Saved: {INDEX_PATH}")
print(f"\n  Total items now: {len(items)}")

# ============================================================
# SUMMARY LOG
# ============================================================
log = ["=== PRICE FIXES ==="] + fixed + ["\n=== ADDED PRODUCTS ==="] + added
with open(r"c:\Movies\quotation-ai\quotation-ai\backend\fix_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print(f"\n=== DONE ===")
print(f"  Fixed: {len(fixed)} prices")
print(f"  Added: {len(added)} products")
print(f"  Log: fix_log.txt")
print(f"\nNext step: Run mongo_push.py to sync to live server")
