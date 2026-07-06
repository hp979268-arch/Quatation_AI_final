import json
with open('search_index_v2.json','r',encoding='utf-8') as f:
    d = json.load(f)
items = d['stored_items']
fixes = {'60080 BS': ('CH', 4400), '750080 BS': ('CH', 5000), '90080 BS': ('CH', 6100)}
for item in items:
    bc = item.get('base_code','')
    vc = item.get('variant_code','')
    if bc in fixes and vc == fixes[bc][0]:
        old = item['price']
        item['price'] = str(fixes[bc][1])
        sc = item.get('search_code','?')
        print(f'FIXED: {sc} | {old} -> {fixes[bc][1]}')
with open('search_index_v2.json','w',encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False)
print('Saved.')
