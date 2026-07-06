"""
STEP 1: Revert all 182 wrong fixes using the log file
STEP 2: Re-apply with CORRECT logic:
  - Model listing line MRP = CP price
  - Size line / standalone MRP after description = Special finish price (BRG/BG/GG/MB/RG)

Confirmed by user: 5141 BRG/BG/GG/MB = Rs.39,500 (size line MRP)
                   5141 CP = Rs.29,500 (model line MRP)
"""

import json

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
LOG_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_price_fix_log.json'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(LOG_PATH, 'r', encoding='utf-8') as f:
    fix_log = json.load(f)

products = data['stored_items']

# Build reverse lookup: base+finish -> old_price
revert_map = {}
for entry in fix_log:
    key = (entry['base'], entry['finish'])
    revert_map[key] = entry['old_price']

reverted = 0
for i, p in enumerate(products):
    base = str(p.get('base_code', '')).strip()
    finish = str(p.get('variant_code', '')).strip().upper()
    key = (base, finish)
    if key in revert_map:
        old_price = revert_map[key]
        current = str(p.get('price', ''))
        products[i]['price'] = old_price
        reverted += 1

print(f"Reverted {reverted} entries back to original prices")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print("Index restored to pre-fix state.")
print("Now re-running correct extraction...")
