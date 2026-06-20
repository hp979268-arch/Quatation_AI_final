import json
import fitz
import re

def fix_aquant_prices():
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    # We need to find all Aquant products with price < 1000
    bad_codes = set()
    for i in db['stored_items']:
        if i.get('brand') == 'Aquant':
            p = str(i.get('price', '0'))
            if p.isdigit() and int(p) < 1000:
                bad_codes.add(i['search_code'])

    if not bad_codes:
        print("No bad prices found.")
        return

    doc = fitz.open(r"uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf")
    blocks = []
    for p in doc:
        for b in p.get_text('blocks'):
            clean_text = b[4].replace('\x03', ' ').strip()
            blocks.append(clean_text)
            
    # Now, for each bad code, let's find its base code (e.g., '2748 BRG' -> '2748')
    # and find the block containing it.
    
    fixes = {}
    
    for code in bad_codes:
        parts = code.split(' ')
        base_code = parts[0] # e.g. 2748
        
        # Find the block containing the special finishes for this base code
        # e.g., "2748 BRG - Brushed Rose Gold"
        
        found_price = None
        for i, block_text in enumerate(blocks):
            if f"{base_code} BRG" in block_text or f"{base_code} BG" in block_text or f"{code}" in block_text:
                # Look backwards for the nearest MRP
                for j in range(i, max(-1, i-5), -1):
                    prev_block = blocks[j]
                    # Find all MRPs in the block
                    mrps = re.findall(r'MRP\s*:\s*[`₹]?\s*([\d,]+)', prev_block)
                    if mrps:
                        # Convert to int
                        vals = [int(m.replace(',', '')) for m in mrps]
                        valid_vals = [v for v in vals if v > 1000]
                        if valid_vals:
                            # For special finishes, it's usually the highest price or the first price in the previous block
                            found_price = str(max(valid_vals))
                            break
                if found_price:
                    break
                    
        if found_price:
            fixes[code] = found_price
        else:
            print(f"Could not find price for {code}")
            
    # Apply fixes
    changed = 0
    for i in db['stored_items']:
        code = i.get('search_code')
        if code in fixes:
            old_price = i.get('price')
            i['price'] = fixes[code]
            print(f"Fixed {code}: {old_price} -> {fixes[code]}")
            changed += 1
            
    if changed > 0:
        with open('search_index_v2.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        print(f"Applied {changed} fixes. Updating MongoDB...")
        from mongodb import get_db
        mongo_db = get_db()
        if mongo_db is not None:
            mongo_db.search_index_v2.replace_one({}, db, upsert=True)
            print("MongoDB updated.")

if __name__ == '__main__':
    fix_aquant_prices()
