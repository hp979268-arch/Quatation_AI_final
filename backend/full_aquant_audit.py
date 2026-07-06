"""
Full Aquant Catalog Final Audit - Fixed version
"""
import json, os

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
IMG_DIR    = r'C:\Movies\quotation-ai\quotation-ai\backend\static\images\Aquant'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['stored_items']
img_files = set(os.listdir(IMG_DIR))
aquant = [p for p in products if str(p.get('brand','')).lower() == 'aquant']

from collections import defaultdict
groups = defaultdict(list)
for p in aquant:
    base = str(p.get('base_code', p.get('name','?'))).strip()
    groups[base].append(p)

SPECIAL = {'BRG','BG','GG','MB','RG','WG','AB','G','BSS'}

issues = {
    'zero_price':    [],
    'bad_price':     [],
    'sf_eq_cp':      [],
    'no_image':      [],
    'img_missing':   [],
    'duplicate':     [],
}

seen_names = {}

for base, variants in sorted(groups.items()):
    cp_entry = next((v for v in variants if str(v.get('variant_code','')).upper()=='CP'), None)
    cp_price_s = str(cp_entry.get('price','0')).replace(',','').strip() if cp_entry else '0'
    try:
        cp_price = float(cp_price_s)
    except:
        cp_price = None

    for v in variants:
        name   = str(v.get('name',''))
        finish = str(v.get('variant_code','')).upper()
        price_s = str(v.get('price','0')).replace(',','').strip()
        images  = v.get('images', [])

        # Duplicate
        key = name.strip().lower()
        if key in seen_names:
            issues['duplicate'].append(f"  {name}")
        else:
            seen_names[key] = True

        # Price check (handle float prices like "26250.00")
        try:
            price = float(price_s)
        except:
            price = 0.0

        if price == 0:
            issues['zero_price'].append(f"  {base} {finish}: Rs.0  | name: {name[:50]}")
        elif price < 500:
            issues['bad_price'].append(f"  {base} {finish}: Rs.{price} (very low?)")
        elif price > 500000:
            issues['bad_price'].append(f"  {base} {finish}: Rs.{price:,.0f} (very high?)")

        # Special finish == CP price
        if finish in SPECIAL and cp_price and price == cp_price:
            issues['sf_eq_cp'].append(f"  {base} {finish}: Rs.{price:,.0f} == CP Rs.{cp_price:,.0f}")

        # Image checks
        if not images:
            issues['no_image'].append(f"  {base} {finish} | {name[:50]}")
        else:
            for img_url in images:
                fname = img_url.split('/')[-1].split('?')[0]
                if fname and fname not in img_files:
                    issues['img_missing'].append(f"  {base} {finish}: '{fname}' NOT ON DISK")

# Report
sections = [
    ('ZERO/MISSING PRICES',                          'zero_price'),
    ('SUSPICIOUS PRICES (<500 or >500,000)',          'bad_price'),
    ('SPECIAL FINISH SAME AS CP (possibly wrong)',    'sf_eq_cp'),
    ('PRODUCTS WITH NO IMAGE URL',                   'no_image'),
    ('IMAGE FILE NOT FOUND ON DISK',                 'img_missing'),
    ('DUPLICATE ENTRIES',                            'duplicate'),
]

grand_total = 0
for title, key in sections:
    items = issues[key]
    grand_total += len(items)
    status = "CLEAN" if not items else f"{len(items)} ISSUES"
    print(f"\n{'='*70}")
    print(f"[{title}]  --  {status}")
    print(f"{'='*70}")
    if items:
        for line in items[:40]:
            print(line)
        if len(items) > 40:
            print(f"  ... and {len(items)-40} more")
    else:
        print("  All good!")

print()
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"  Total Aquant entries    : {len(aquant)}")
print(f"  Total base products     : {len(groups)}")
print(f"  Total images on disk    : {len(img_files)}")
print(f"  TOTAL ISSUES FOUND      : {grand_total}")
if grand_total == 0:
    print("  STATUS: CATALOG IS CLEAN!")
else:
    print("  STATUS: ISSUES NEED ATTENTION")
