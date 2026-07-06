import json
with open('search_index_v2.json','r',encoding='utf-8') as f:
    d = json.load(f)
items = d['stored_items']
ki = d.get('keyword_index',{})

r = [i for i in items if i.get('base_code','') in ('30006','30007')]
print(f'Total 30006/30007 items: {len(r)}')
print()
for i in sorted(r, key=lambda x: (x.get('base_code',''), x.get('variant_code',''))):
    sc = i.get('search_code','')
    price = i.get('price','')
    name = i.get('name','')[:50]
    img = i.get('images',['NO IMG'])[0] if i.get('images') else 'NO IMG'
    img_file = img.split('/')[-1].split('?')[0]
    print(f'  {sc:20} | {price:6} | {name}')
    print(f'                       | img: {img_file}')

# Check keyword index
print()
print('Keyword index entries for 30006/30007:')
for k in sorted(ki.keys()):
    if '30006' in k or '30007' in k:
        print(f'  key={k:30} -> {len(ki[k])} results')
