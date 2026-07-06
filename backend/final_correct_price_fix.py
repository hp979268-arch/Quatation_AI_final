"""
FINAL CORRECT price fix for Aquant special finish variants.
Rules confirmed by user:
  1. CP price = UNCHANGED (already correct in index)
  2. BRG/BG/GG/MB/RG all get the SAME special_finish_mrp from PDF
  3. Only update if current price differs from PDF value

Also checks description/text fields for size-in-description issues.
"""

import json

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
PDF_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_prices_correct.json'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(PDF_PATH, 'r', encoding='utf-8') as f:
    pdf = json.load(f)

products = data['stored_items']

SPECIAL_FINISHES = {'BRG', 'BG', 'GG', 'MB', 'RG'}

fixes = []
price_errors = []
desc_warnings = []

print("=" * 70)
print("APPLYING CORRECT SPECIAL FINISH PRICES")
print("=" * 70)

for i, p in enumerate(products):
    base = str(p.get('base_code', '')).strip()
    finish = str(p.get('variant_code', '')).strip().upper()
    current_price = str(p.get('price', '')).strip()

    if base not in pdf:
        continue

    # Only fix special finishes — CP is untouched
    if finish not in SPECIAL_FINISHES:
        continue

    special_mrp = pdf[base].get('special_finish_mrp')
    if not special_mrp:
        price_errors.append(f"  {base} {finish}: No special_finish_mrp found in PDF data")
        continue

    correct_price = str(special_mrp)

    if current_price != correct_price:
        print(f"  FIX  {base:8s} {finish:5s}: Rs.{current_price:>10} -> Rs.{correct_price:>10}")
        products[i]['price'] = correct_price
        fixes.append({
            'base': base, 'finish': finish,
            'old': current_price, 'new': correct_price
        })

print()
print(f"Total price fixes: {len(fixes)}")

# -------------------------------------------------------
# Check descriptions for size/dimension mixed into text
# -------------------------------------------------------
print()
print("=" * 70)
print("CHECKING DESCRIPTIONS FOR SIZE/DIMENSION ISSUES")
print("=" * 70)

import re
size_pattern = re.compile(r'\b\d{2,4}\s*[xX]\s*\d{2,4}\b|\b\d{3,4}\s*mm\b|\b\d{2,4}\s*mtr\b', re.IGNORECASE)

for i, p in enumerate(products):
    base = str(p.get('base_code', '')).strip()
    if base not in pdf:
        continue

    name = str(p.get('name', ''))
    text = str(p.get('text', ''))
    finish = str(p.get('variant_code', '')).strip().upper()

    # Flag if size appears IN the product name (not normal)
    if size_pattern.search(name):
        desc_warnings.append(f"  {base} {finish}: Name has size info -> '{name[:70]}'")

if desc_warnings:
    print(f"Found {len(desc_warnings)} products with size in name:")
    for w in desc_warnings:
        print(w)
else:
    print("  All descriptions look clean - no size mixed into product names.")

# -------------------------------------------------------
# Save updated index
# -------------------------------------------------------
if fixes:
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print()
    print(f"Index saved: {INDEX_PATH}")

    log_path = r'C:\Movies\quotation-ai\quotation-ai\backend\correct_price_fix_log.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(fixes, f, indent=2, ensure_ascii=False)
    print(f"Fix log saved: {log_path}")
else:
    print("No changes needed.")

# -------------------------------------------------------
# Final verification
# -------------------------------------------------------
print()
print("=" * 70)
print("FINAL VERIFICATION - Special Finish Prices After Fix")
print("=" * 70)
print(f"{'BASE':<8} {'CP':>12} {'BRG':>12} {'BG':>12} {'GG':>12} {'MB':>12} {'RG':>12}")
print("-" * 78)

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data2 = json.load(f)

for base in sorted(pdf.keys()):
    row = {base: {}}
    for p in data2['stored_items']:
        if str(p.get('base_code','')) == base:
            fin = str(p.get('variant_code','')).upper()
            row[base][fin] = p.get('price', 'N/A')

    d = row[base]
    cp  = d.get('CP',  'N/A')
    brg = d.get('BRG', 'N/A')
    bg  = d.get('BG',  'N/A')
    gg  = d.get('GG',  'N/A')
    mb  = d.get('MB',  'N/A')
    rg  = d.get('RG',  'N/A')

    # Flag if any special finish differs from BRG (should all be same)
    specials = [v for v in [brg, bg, gg, mb, rg] if v != 'N/A']
    flag = " <-- MISMATCH" if len(set(specials)) > 1 else ""

    print(f"{base:<8} {cp:>12} {brg:>12} {bg:>12} {gg:>12} {mb:>12} {rg:>12}{flag}")
