import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('search_index_v2.json','r',encoding='utf-8') as f:
    d = json.load(f)
items = d['stored_items']
ki = d.get('keyword_index', {})

# Find all 30006/30007 item positions and rebuild their keyword entries
for pos, item in enumerate(items):
    bc = item.get('base_code','')
    if bc not in ('30006','30007'):
        continue
    vc = item.get('variant_code','').lower()
    sc = item.get('search_code','').lower()

    # Keys to register this item under
    keys_to_add = [
        bc,                          # "30006" or "30007"
        bc + vc,                     # "30006cp", "30007brg" etc
        sc.replace(' ',''),          # "30006cp"
        '30006-30007',               # combined search
        'extendibleshowerhose',
        'showerhose',
        'hose',
    ]
    if '1.0' in item.get('name','') or bc == '30006':
        keys_to_add += ['1mtr','1.0mtr','1meter']
    if '1.5' in item.get('name','') or bc == '30007':
        keys_to_add += ['1.5mtr','15mtr','1.5meter']

    for k in keys_to_add:
        k = k.strip().lower()
        if not k:
            continue
        if k not in ki:
            ki[k] = []
        if pos not in ki[k]:
            ki[k].append(pos)

d['keyword_index'] = ki
with open('search_index_v2.json','w',encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False)

# Verify
print("30006 keyword key results:", len(ki.get('30006',[])))
print("30007 keyword key results:", len(ki.get('30007',[])))
print("30006-30007 key results:", len(ki.get('30006-30007',[])))
print("hose key results:", len(ki.get('hose',[])))
print("1mtr key results:", len(ki.get('1mtr',[])))
print("1.5mtr key results:", len(ki.get('1.5mtr',[])))
print("\nDone - keyword index updated.")
