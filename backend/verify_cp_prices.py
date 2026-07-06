import json

with open('search_index_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
products = data['stored_items']

# CP prices confirmed by user
user_confirmed = {
    '2113':  85000,
    '2564':  19750,
    '2641':  10500,
    '2642':  12500,
    '2644':  14500,
    '28118':  3900,
    '28202':  3000,
    '4051':  16000,
    '4052':  16000,
    '5104':  27750,
    '5105':  32500,
    '5122':  99500,
    '5123': 149000,
    '5141':  29500,
}

print(f"{'BASE':<8} {'USER CONFIRMED':>15} {'IN INDEX':>15}   STATUS")
print('-' * 58)

all_ok = True
for base, user_price in sorted(user_confirmed.items()):
    cp = next((p for p in products 
               if str(p.get('base_code',''))==base 
               and str(p.get('variant_code','')).upper()=='CP'), None)
    if cp:
        idx_price_str = str(cp.get('price','0')).replace(',','').strip()
        try:
            idx_price = int(idx_price_str)
        except:
            idx_price = -1
        if idx_price == user_price:
            status = 'OK'
        else:
            status = '*** MISMATCH ***'
            all_ok = False
        print(f"{base:<8} {user_price:>15,} {idx_price:>15,}   {status}")
    else:
        print(f"{base:<8} {user_price:>15,} {'NOT FOUND':>15}   *** MISSING ***")
        all_ok = False

print()
if all_ok:
    print('ALL CP PRICES MATCH PERFECTLY. No issues.')
else:
    print('MISMATCHES FOUND - Action needed!')
