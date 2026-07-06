import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('search_index_v2.json','r',encoding='utf-8') as f:
    d = json.load(f)
items = d['stored_items']

def get_variants(base):
    return {i.get('variant_code','').upper(): i.get('price') 
            for i in items if i.get('base_code','').upper() == base.upper()}

print("=== REMAINING ISSUES CHECK ===\n")

# 1. 2563 GG/MB/RG - should all be 36750 (PDF pg24 says all non-CP = 36750)
print("1. 2563 variants (all non-CP should be 36750):")
for vc, p in get_variants('2563').items():
    flag = " !!WRONG" if vc in ('GG','MB','RG') and str(p) != '36750' else " OK"
    print(f"   2563 {vc:5} = {p}{flag}")

# 2. 1419 - check all variants
print("\n2. 1419 variants (non-CP should be 8250):")
for vc, p in sorted(get_variants('1419').items()):
    print(f"   1419 {vc:5} = {p}")

# 3. 1186 - check all variants  
print("\n3. 1186 variants (non-CP should be 5250):")
for vc, p in sorted(get_variants('1186').items()):
    print(f"   1186 {vc:5} = {p}")

# 4. 2741 RG - check
print("\n4. 2741 variants:")
for vc, p in sorted(get_variants('2741').items()):
    print(f"   2741 {vc:5} = {p}")

# 5. 1418 RG
print("\n5. 1418 variants (RG should be present):")
for vc, p in sorted(get_variants('1418').items()):
    print(f"   1418 {vc:5} = {p}")

# 6. 1424-200 and 1424-500 CP
print("\n6. 1424-200 and 1424-500 (CP should be present):")
for base in ['1424-200','1424-500']:
    for vc, p in sorted(get_variants(base).items()):
        print(f"   {base} {vc:5} = {p}")

# 7. 1936/1902 SM - missing
print("\n7. 1936/1902 SM (Statuario Matt) - should exist:")
for base in ['1936','1902']:
    vs = get_variants(base)
    print(f"   {base} variants: {list(vs.keys())}")
    if 'SM' not in vs:
        print(f"   !! SM variant MISSING for {base}")

# 8. 1025 - dashboard check
print("\n8. 1025 AquaBliss:")
r = [i for i in items if i.get('base_code','') == '1025']
for i in r:
    print(f"   {i.get('search_code')} | price={i.get('price')} | cat={i.get('category','')} | img={i.get('images',[''])[0][:40]}")

# 9. Any items with price = 0 or empty
print("\n9. Items with price=0 or empty (sample):")
zeros = [i for i in items if str(i.get('price','0')).strip() in ('0','','None') and i.get('brand') == 'Aquant']
print(f"   Total zero/empty price Aquant items: {len(zeros)}")
for i in zeros[:5]:
    print(f"   {i.get('search_code')} | {i.get('price')}")

# 10. 2569 CP price check
print("\n10. 2569 CP (should be 110000):", get_variants('2569').get('CP','NOT FOUND'))
