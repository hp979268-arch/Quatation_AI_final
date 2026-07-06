import json

def audit_aquant_prices_2():
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('stored_items', [])
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
        if 'CP' in variants:
            cp_price = variants['CP']
            for sf in special_finishes:
                if sf in variants:
                    sf_price = variants[sf]
                    if sf_price < cp_price:
                        issues.append(f"{base_code} {sf} price ({sf_price}) is LESS than CP price ({cp_price})")
                    elif sf_price > 3 * cp_price:
                        issues.append(f"{base_code} {sf} price ({sf_price}) is MORE THAN 3X CP price ({cp_price})")

    with open('aquant_audit_issues_2.txt', 'w', encoding='utf-8') as f:
        for issue in issues:
            f.write(issue + '\n')
            
    print(f"Total base codes: {len(products)}")
    print(f"Found {len(issues)} new potential issues.")

if __name__ == '__main__':
    audit_aquant_prices_2()
