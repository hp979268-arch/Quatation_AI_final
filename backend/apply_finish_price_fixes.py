"""
Fix wrong prices in search_index_v2.json for Aquant special finish products.
Based on verified prices extracted directly from Aquant Price List Vol 15. Feb 2026 PDF.

Rules (confirmed from PDF format):
- BRG, BG, GG, MB all share the SAME MRP (this is correct per PDF)
- RG = same as special finish MRP unless separately listed
- CP has its own separate MRP

Only fixing products where WRONG values crept in from other products.
Also fixing products where the extracted price was the CP price instead of special finish price.
"""

import json
import copy

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
PDF_PRICES_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_prices_from_pdf.json'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(PDF_PRICES_PATH, 'r', encoding='utf-8') as f:
    pdf_prices = json.load(f)

products = data['stored_items']

# Make a backup reference
original_products = copy.deepcopy(products)

SPECIAL_FINISHES = {'BRG', 'BG', 'GG', 'MB', 'RG'}
CP_FINISHES = {'CP'}

fixes_applied = []
errors = []

for i, product in enumerate(products):
    base = str(product.get('base_code', '')).strip()
    finish = str(product.get('variant_code', '')).strip().upper()
    current_price = str(product.get('price', '')).strip()
    
    if base not in pdf_prices:
        continue
    
    pdf = pdf_prices[base]
    special_mrp = pdf.get('special_finish_mrp')
    cp_mrp = pdf.get('cp_mrp')
    
    correct_price = None
    
    if finish in SPECIAL_FINISHES:
        # All special finishes should have special_finish_mrp
        correct_price = special_mrp
    elif finish in CP_FINISHES:
        # CP should have cp_mrp (but only update if cp_mrp is available)
        if cp_mrp:
            correct_price = cp_mrp
    
    if correct_price is None:
        continue
    
    correct_price_str = str(correct_price)
    
    if current_price != correct_price_str:
        print(f"FIX: {base} {finish:4s} | Was: Rs.{current_price:>10} -> Correct: Rs.{correct_price_str:>10}")
        products[i]['price'] = correct_price_str
        fixes_applied.append({
            'base': base,
            'finish': finish,
            'old_price': current_price,
            'new_price': correct_price_str
        })

print()
print("=" * 60)
print(f"Total fixes applied: {len(fixes_applied)}")

if fixes_applied:
    # Save updated index
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"Updated: {INDEX_PATH}")
    
    # Save fix log
    log_path = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_price_fix_log.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(fixes_applied, f, indent=2, ensure_ascii=False)
    print(f"Fix log: {log_path}")
else:
    print("No changes made.")
