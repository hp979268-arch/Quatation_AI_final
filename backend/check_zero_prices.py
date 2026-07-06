import json
with open('search_index_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
products = data['stored_items']

for p in products:
    if str(p.get('brand','')).lower() == 'aquant':
        bc = str(p.get('base_code',''))
        vc = str(p.get('variant_code',''))
        price = str(p.get('price',''))
        if bc in ['1461','1485']:
            print('base:', bc, '| variant:', vc, '| price:', price)
            print('name:', p.get('name','')[:80])
            # Show page number and source
            print('page:', p.get('page','?'), '| source:', str(p.get('source',''))[:50])
            print()
