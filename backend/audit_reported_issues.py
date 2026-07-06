import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data["stored_items"]  # list of dicts

def find_prefix(p):
    p = p.upper()
    results = []
    for i in items:
        sc = i.get("search_code","").upper().replace(" ","")
        bc = i.get("base_code","").upper().replace(" ","")
        vc = i.get("variant_code","").upper().replace(" ","")
        code_full = (bc + vc).upper()
        if code_full.startswith(p) or sc.startswith(p):
            results.append(i)
    return results

def find_base(b):
    b = b.upper()
    return [i for i in items if i.get("base_code","").upper() == b]

def fmt(i):
    sc = i.get("search_code", i.get("base_code","?") + " " + i.get("variant_code",""))
    return f"    search_code={sc} | price={i.get('price',0)} | finish={i.get('finish_label','')} | name={i.get('name','')[:40]}"

out = []
def sec(t): out.append(f"\n{'='*65}\n  {t}\n{'='*65}")
def ok(m): out.append(f"  [OK] {m}")
def warn(m): out.append(f"  [!!] {m}")
def info(m): out.append(f"  [--] {m}")

# Helper: check if non-CP finishes have same price as CP (indicates price mismatch)
def check_cp_mismatch(its, label):
    cp = [i for i in its if i.get("variant_code","").upper() in ("CP","")]
    non_cp = [i for i in its if i.get("variant_code","").upper() not in ("CP","")]
    cp_prices = list(set(i.get("price","0") for i in cp))
    non_cp_prices = list(set(i.get("price","0") for i in non_cp))
    info(f"{label}: CP prices={cp_prices}, Non-CP prices={non_cp_prices}")
    if cp_prices and non_cp_prices and set(cp_prices) == set(non_cp_prices):
        warn(f"PRICE MISMATCH CONFIRMED: Non-CP variants share same price as CP for {label}!")
    elif not non_cp:
        warn(f"No non-CP variants found for {label}")
    else:
        ok(f"Prices differ between CP and non-CP for {label} (may be correct)")

# ---- PG-20: 30006/30007 G-Gold, 1.5m missing ----
sec("PG-20 & PG-43: 30006/30007 -- 1.5m variant missing from dashboard")
all_30006 = find_base("30006")
all_30007 = find_base("30007")
all_30 = all_30006 + all_30007
info(f"Total 30006 items: {len(all_30006)}, 30007 items: {len(all_30007)}")
for i in all_30: out.append(fmt(i))
m15 = [i for i in all_30 if "1.5" in str(i.get("name","")) or "1.5" in str(i.get("text",""))]
if m15:
    ok(f"1.5m variants FOUND: {len(m15)}")
    for i in m15: out.append(fmt(i))
else:
    warn("NO 1.5m variant found in name/text for 30006/30007 -- CONFIRMED MISSING")

# ---- PG-20: 2592 GG/MB/RG ----
sec("PG-20: 2592 GG/MB/RG -- price mismatch")
its = find_base("2592")
info(f"Total 2592 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2592")
else: warn("NOT FOUND: 2592")

# ---- PG-23: 2562 ----
sec("PG-23: 2562 GG/MB/RG -- price mismatch")
its = find_base("2562")
info(f"Total 2562 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2562")
else: warn("NOT FOUND: 2562")

# ---- PG-24: 2563 ----
sec("PG-24: 2563 GG/MB/RG -- price mismatch")
its = find_base("2563")
info(f"Total 2563 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2563")
else: warn("NOT FOUND: 2563")

# ---- PG-24: 3161 ----
sec("PG-24: 3161 GG/MB/RG -- price mismatch")
its = find_base("3161")
info(f"Total 3161 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "3161")
else: warn("NOT FOUND: 3161")

# ---- PG-25: 3162 ----
sec("PG-25: 3162 BRG (all except CP) -- price mismatch")
its = find_base("3162")
info(f"Total 3162 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "3162")
else: warn("NOT FOUND: 3162")

# ---- PG-25: 3163 ----
sec("PG-25: 3163 (all except CP) -- price mismatch")
its = find_base("3163")
info(f"Total 3163 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "3163")
else: warn("NOT FOUND: 3163")

# ---- PG-25/26: 2569 ----
sec("PG-25/26: 2569 BRG variants -- price mismatch")
its = find_base("2569")
info(f"Total 2569 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2569")
else: warn("NOT FOUND: 2569")

# ---- PG-26/28: 2122 ----
sec("PG-26/28: 2122 (all except CP) -- price mismatch")
its = find_base("2122")
info(f"Total 2122 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2122")
else: warn("NOT FOUND: 2122")

# ---- PG-29: 2114 ----
sec("PG-29: 2114 GG/MB/RG -- price mismatch")
its = find_base("2114")
info(f"Total 2114 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2114")
else: warn("NOT FOUND: 2114")

# ---- PG-30: 2104 ----
sec("PG-30: 2104 GG/MB/RG -- price mismatch")
its = find_base("2104")
info(f"Total 2104 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2104")
else: warn("NOT FOUND: 2104")

# ---- PG-30: 2106 ----
sec("PG-30: 2106 GG/MB/RG -- price mismatch")
its = find_base("2106")
info(f"Total 2106 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2106")
else: warn("NOT FOUND: 2106")

# ---- PG-30/31: 2102 ----
sec("PG-30/31: 2102 (all) -- price mismatch")
its = find_base("2102")
info(f"Total 2102 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 2102")

# ---- PG-31: 1411, 1415, 1418, 1419 ----
for base in ["1411","1415","1418","1419"]:
    sec(f"PG-31: {base} (all) -- price mismatch / missing from dashboard")
    its = find_base(base)
    info(f"Total {base} items: {len(its)}")
    for i in its: out.append(fmt(i))
    if its: check_cp_mismatch(its, base)
    else: warn(f"NOT FOUND: {base}")

# ---- PG-31/91: 1507 ----
sec("PG-31/91: 1507 (all except BSS) -- price mismatch")
its = find_base("1507")
info(f"Total 1507 items: {len(its)}")
for i in its: out.append(fmt(i))
non_bss = [i for i in its if "BSS" not in i.get("variant_code","").upper()]
bss = [i for i in its if "BSS" in i.get("variant_code","").upper()]
info(f"Non-BSS: {len(non_bss)}, BSS: {len(bss)}")
if non_bss and bss:
    info(f"Non-BSS prices: {list(set(i.get('price') for i in non_bss))}")
    info(f"BSS prices:     {list(set(i.get('price') for i in bss))}")
if not its: warn("NOT FOUND: 1507")

# ---- PG-91: 1501 ----
sec("PG-91: 1501 -- price mismatch")
its = find_base("1501")
info(f"Total 1501 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 1501")

# ---- Seat Covers ----
sec("Seat Covers: PVC, UF, Colour UF")
seat = [i for i in items if "seat" in i.get("name","").lower() or "seat" in i.get("category","").lower()]
info(f"Total seat cover items found: {len(seat)}")
for i in seat[:20]: out.append(fmt(i))
if len(seat) > 20: info(f"...and {len(seat)-20} more seat items")
if not seat: warn("NO seat cover items found in index!")

# ---- PG-90: 1025 AquaBliss ----
sec("PG-90: 1025-AquaBliss -- missing from dashboard")
its = find_base("1025")
if its:
    ok(f"1025 found: {len(its)} items")
    for i in its: out.append(fmt(i))
else:
    warn("1025 NOT FOUND in index -- CONFIRMED MISSING")

# ---- PG-90: 1506 ----
sec("PG-90: 1506 -- price mismatch")
its = find_base("1506")
info(f"Total 1506 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 1506")

# ---- PG-86: 1947 ----
sec("PG-86: 1947 -- price mismatch")
its = find_base("1947")
info(f"Total 1947 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 1947")

# ---- PG-85: 1936SM, 1902SM ----
sec("PG-85: 1936SM, 1902SM -- price mismatch")
for base in ["1936","1902"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if not its: warn(f"NOT FOUND: {base}")

# ---- PG-77: 9057 Konig ----
sec("PG-77: 9057-Konig -- price mismatch")
its = find_base("9057")
info(f"Total 9057 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 9057")

# ---- PG-63: 1151, 1152, 1153 ----
sec("PG-63: 1151, 1152, 1153 -- price mismatch")
for base in ["1151","1152","1153"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if not its: warn(f"NOT FOUND: {base}")

# ---- PG-63: 1460, 1487, 1461, 1462, 1010 ----
sec("PG-63: 1460, 1487, 1461, 1462, 1010 -- price mismatch")
for base in ["1460","1487","1461","1462","1010"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if not its: warn(f"NOT FOUND: {base}")

# ---- PG-61: 28088 ----
sec("PG-61: 28088 -- price mismatch")
its = find_base("28088")
info(f"Total 28088 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 28088")

# ---- PG-59: 1318, 1319, 1320, 1436, 1437 ----
sec("PG-59: 1318, 1319, 1320, 1436, 1437 -- price mismatch")
for base in ["1318","1319","1320","1436","1437"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if not its: warn(f"NOT FOUND: {base}")

# ---- PG-58: 60080BSCH, 90080BSCH, 750080BSCH ----
sec("PG-58: 60080BSCH, 90080BSCH, 750080BSCH -- price mismatch")
for code in ["60080BSCH","90080BSCH","750080BSCH"]:
    # try search_code match
    matches = [i for i in items if code.upper() in i.get("search_code","").upper().replace(" ","")]
    if not matches:
        base = code.replace("BSCH","")
        matches = find_base(base)
    info(f"{code}: {len(matches)} items")
    for i in matches: out.append(fmt(i))
    if not matches: warn(f"NOT FOUND: {code}")

# ---- PG-57: 1439 Fleur ----
sec("PG-57: 1439-Fleur -- price mismatch")
its = find_base("1439")
info(f"Total 1439 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 1439")

# ---- PG-56: 1258, 1256, 1245, 1257 ----
sec("PG-56: 1258-Revive, 1256-Eden, 1245-Divine, 1257-Retro -- price mismatch")
for base in ["1258","1256","1245","1257"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if not its: warn(f"NOT FOUND: {base}")

# ---- PG-54: 1155, 28197, 28198 ----
sec("PG-54: 1155, 28197, 28198 -- price mismatch")
for base in ["1155","28197","28198"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if not its: warn(f"NOT FOUND: {base}")

# ---- PG-52: 1485 ----
sec("PG-52: 1485 -- price mismatch")
its = find_base("1485")
info(f"Total 1485 items: {len(its)}")
for i in its: out.append(fmt(i))
if not its: warn("NOT FOUND: 1485")

# ---- PG-48: 2750, 2741 ----
sec("PG-48: 2750, 2741 (all except CP) -- price mismatch")
for base in ["2750","2741"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if its: check_cp_mismatch(its, base)
    else: warn(f"NOT FOUND: {base}")

# ---- PG-47: 2728, 2726, 2729 ----
sec("PG-47: 2728, 2726, 2729 (all except CP) -- price mismatch")
for base in ["2728","2726","2729"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if its: check_cp_mismatch(its, base)
    else: warn(f"NOT FOUND: {base}")

# ---- PG-46: 2721 ----
sec("PG-46: 2721 (all except CP) -- price mismatch")
its = find_base("2721")
info(f"Total 2721 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "2721")
else: warn("NOT FOUND: 2721")

# ---- PG-45: 1472 ----
sec("PG-45: 1472 (all except CP) -- price mismatch")
its = find_base("1472")
info(f"Total 1472 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "1472")
else: warn("NOT FOUND: 1472")

# ---- PG-44: 2650, 7011 ----
sec("PG-44: 2650, 7011 (all except CP) -- price mismatch")
for base in ["2650","7011"]:
    its = find_base(base)
    info(f"{base}: {len(its)} items")
    for i in its: out.append(fmt(i))
    if its: check_cp_mismatch(its, base)
    else: warn(f"NOT FOUND: {base}")

# ---- PG-43: 1186 missing from dashboard ----
sec("PG-43: 1186 (all except CP) -- missing from dashboard")
its = find_base("1186")
if its:
    ok(f"1186 found in index: {len(its)} items -- BUT user says missing from dashboard")
    for i in its: out.append(fmt(i))
else:
    warn("1186 NOT FOUND in index at all -- CONFIRMED MISSING")

# ---- PG-42: 1125 ----
sec("PG-42: 1125 (all except CP) -- price mismatch")
its = find_base("1125")
info(f"Total 1125 items: {len(its)}")
for i in its: out.append(fmt(i))
if its: check_cp_mismatch(its, "1125")
else: warn("NOT FOUND: 1125")

# ---- PG-40: 1424 ----
sec("PG-40: 1424-200, 1424-500 (all) -- BEV CP price mismatch + missing from dashboard")
its = find_base("1424")
if its:
    ok(f"1424 found: {len(its)} items")
    for i in its: out.append(fmt(i))
    # Check BEV vs CP
    bev = [i for i in its if "BEV" in i.get("variant_code","").upper()]
    cp_1424 = [i for i in its if i.get("variant_code","").upper() == "CP"]
    info(f"BEV variants: {len(bev)}, CP variants: {len(cp_1424)}")
    if bev: info(f"BEV prices: {list(set(i.get('price') for i in bev))}")
    if cp_1424: info(f"CP prices:  {list(set(i.get('price') for i in cp_1424))}")
else:
    warn("1424 NOT FOUND in index -- CONFIRMED MISSING")

# ---- SUMMARY ----
sec("SUMMARY STATS")
total = len(items)
zero_p = [i for i in items if not i.get("price") or str(i.get("price","0")).strip() in ("","0","0.0")]
info(f"Total items in index: {total}")
info(f"Items with price=0 or missing: {len(zero_p)}")

result = "\n".join(out)
print(result)
out_path = r"c:\Movies\quotation-ai\quotation-ai\backend\audit_issues_output.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result)
print(f"\n[Saved to {out_path}]")
