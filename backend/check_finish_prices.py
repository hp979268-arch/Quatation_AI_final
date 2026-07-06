import json

index_path = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
with open(index_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
products = data['stored_items']

reported_groups = {
    '5141': ['BRG','BG','GG','MB'],
    '4051': ['BRG','BG','GG','MB','RG'],
    '4052': ['GG','MB','RG'],
    '5123': ['BRG','BG','GG','MB','RG'],
    '5122': ['BRG','BG','GG','MB','RG'],
    '5105': ['BRG','BG','GG','MB','RG'],
    '5104': ['BRG','BG','GG','MB','RG'],
    '1482': ['BRG','BG','GG','MB','RG'],
    '4006': ['GG','MB','RG'],
    '28192': ['GG','MB','RG'],
    '28202': ['BRG','BG','GG','MB'],
    '1476': ['GG','MB','RG'],
    '1456': ['BRG','BG','GG','MB'],
    '1457': ['BRG','BG','GG','MB','RG'],
    '28201': ['GG','MB'],
    '28118': ['BRG','BG','GG','MB','RG'],
    '28194': ['GG','MB','RG'],
    '1459': ['GG','MB','RG'],
    '1449': ['BRG','BG','GG','MB','RG'],
    '1477': ['GG','MB','RG'],
    '1479': ['BRG','BG','GG','MB','RG'],
    '1314': ['BRG','BG','GG','MB','RG'],
    '3162': ['BRG','BG','GG','MB','RG'],
    '3163': ['BRG','BG','GG','MB','RG'],
    '3166': ['BRG','BG','GG','MB','RG'],
    '2098': ['BRG','BG','GG','MB','RG'],
    '2096': ['BRG','BG','GG','MB','RG'],
    '2093': ['BRG','BG','GG','MB','RG'],
    '2121': ['BRG','BG','GG','MB','RG'],
    '2113': ['BRG','BG','GG','MB','RG'],
    '2101': ['BRG','BG','GG','MB','RG'],
    '2102': ['BRG','BG','GG','MB','RG'],
    '1411': ['BRG','BG','GG','MB','RG'],
    '1415': ['BRG','BG','GG','MB','RG'],
    '1418': ['BRG','BG','GG','MB'],
    '1419': ['BRG','BG','GG','MB'],
    '2641': ['BRG','BG','GG','MB'],
    '2642': ['BRG','BG','GG','MB'],
    '2644': ['BRG','BG','GG','MB'],
    '2646': ['BRG','BG','GG','MB'],
    '2645': ['BRG','BG','GG','MB'],
    '2591': ['BRG','BG','GG','MB','RG'],
    '2593': ['BRG','BG','GG','MB','RG'],
    '2594': ['BRG','BG','GG','MB','RG'],
    '2561': ['BRG','BG','GG','MB','RG'],
    '2564': ['BRG','BG','GG','MB','RG'],
    '2565': ['BRG','BG','GG','MB','RG'],
    '2566': ['BRG','BG','GG','MB','RG'],
}

# Known wrong prices that belong to other products
KNOWN_WRONG = {'137000', '145000', '165000', '125000', '35500', '39500', '29500'}

print("=" * 70)
print("AQUANT SPECIAL FINISH PRICE AUDIT REPORT")
print("=" * 70)

all_same_price = []
big_ratio = []
known_wrong_price = []
looks_ok = []

for base in sorted(reported_groups.keys()):
    finishes = reported_groups[base]
    prices = {}
    for finish in finishes:
        m = next((p for p in products 
                  if str(p.get('base_code',''))==base and str(p.get('variant_code',''))==finish), None)
        if m:
            prices[finish] = str(m.get('price','N/A'))

    cp = next((p for p in products 
               if str(p.get('base_code',''))==base and str(p.get('variant_code',''))=='CP'), None)
    cp_price = cp.get('price') if cp else 'N/A'

    if not prices:
        continue

    price_vals = list(prices.values())
    unique_prices = set(price_vals)
    
    issues = []
    
    # 1. All same price (lazy copy - should differ per finish)
    if len(unique_prices) == 1:
        issues.append("ALL FINISHES SAME PRICE")
        all_same_price.append(base)
    
    # 2. Known wrong values (cross-contamination from other products)
    for f, p in prices.items():
        if p in KNOWN_WRONG:
            issues.append(f"{f}=Rs.{p} is a KNOWN WRONG VALUE")
            known_wrong_price.append(f"{base}{f}")
    
    # 3. Extreme ratio between finishes
    int_prices = [int(v) for v in price_vals if v.isdigit()]
    if len(int_prices) >= 2:
        ratio = max(int_prices) / min(int_prices)
        if ratio > 4:
            issues.append(f"EXTREME RATIO {ratio:.1f}x between finishes")
            big_ratio.append(base)

    if issues:
        print(f"\nBASE {base} (CP=Rs.{cp_price})")
        for f, p in prices.items():
            marker = " <-- ?" if p in KNOWN_WRONG else ""
            print(f"  {f:6s}: Rs.{p}{marker}")
        print(f"  ISSUE: {' | '.join(issues)}")
    else:
        looks_ok.append(base)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Products where ALL finishes have same price:  {len(set(all_same_price))} products")
print(f"Products with extreme price ratio (>4x):      {len(set(big_ratio))} products")
print(f"Individual variants with known wrong values:  {len(known_wrong_price)} variants")
print(f"Products that look OK:                        {len(looks_ok)} products")
print()
print("All-same-price products:", sorted(set(all_same_price)))
print()
print("Extreme ratio products:", sorted(set(big_ratio)))
