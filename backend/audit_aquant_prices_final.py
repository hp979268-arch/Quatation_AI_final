import json

def audit_aquant_prices():
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('stored_items', [])
    
    # Group by base_code
    products = {}
    for item in items:
        if item.get('brand') == 'Aquant':
            base_code = item.get('base_code', '')
            variant = item.get('variant_code', '')
            price = item.get('price', '0')
            try:
                price_val = float(price.replace(',', '').replace('`', '').strip() or 0)
            except:
                price_val = 0
                
            if base_code not in products:
                products[base_code] = {}
            products[base_code][variant] = price_val

    issues = []
    
    special_finishes = ['BRG', 'BG', 'GG', 'MB', 'RG']
    
    for base_code, variants in products.items():
        # Check for 0 price
        for v, p in variants.items():
            if p == 0:
                issues.append(f"{base_code} {v} has 0 or invalid price")
        
        # If both CP and special finishes exist
        has_special = any(sf in variants for sf in special_finishes)
        if 'CP' in variants and has_special:
            cp_price = variants['CP']
            
            # 1. Special finish price should generally not be equal to CP price
            for sf in special_finishes:
                if sf in variants and variants[sf] == cp_price:
                    issues.append(f"{base_code} {sf} has same price as CP ({cp_price})")
            
            # 2. BRG should usually equal BG
            if 'BRG' in variants and 'BG' in variants:
                if variants['BRG'] != variants['BG']:
                    issues.append(f"{base_code} BRG ({variants['BRG']}) != BG ({variants['BG']})")
                    
            # 3. GG, MB, RG should usually equal each other
            gg_mb_rg = [variants[sf] for sf in ['GG', 'MB', 'RG'] if sf in variants]
            if gg_mb_rg and len(set(gg_mb_rg)) > 1:
                issues.append(f"{base_code} GG/MB/RG prices do not match each other: {gg_mb_rg}")

    with open('aquant_audit_issues.txt', 'w', encoding='utf-8') as f:
        for issue in issues:
            f.write(issue + '\n')
            
    print(f"Total base codes: {len(products)}")
    print(f"Found {len(issues)} potential issues. Check aquant_audit_issues.txt for details.")

if __name__ == '__main__':
    audit_aquant_prices()
