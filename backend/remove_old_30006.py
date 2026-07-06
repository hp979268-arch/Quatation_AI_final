import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('search_index_v2.json','r',encoding='utf-8') as f:
    d = json.load(f)

items = d['stored_items']
before = len(items)

# Remove old combined "30006-30007" entries
new_items = [i for i in items if not (
    i.get('base_code','') == '30006-30007' or
    i.get('search_code','').startswith('30006-30007 ')
)]

removed = before - len(new_items)
print(f"Removed {removed} old combined entries")
print(f"Items: {before} -> {len(new_items)}")

# Rebuild keyword index - remove references to deleted items
# Easiest: rebuild from scratch for 30006/30007 keys
ki = d.get('keyword_index', {})

# Remove old combined keys entirely
keys_to_delete = [k for k in ki if '30006-30007' in k]
for k in keys_to_delete:
    del ki[k]
    print(f"  Removed keyword key: {k}")

# Rebuild position references for remaining items
# (remove any position refs that no longer exist)
max_pos = len(new_items) - 1
for k in list(ki.keys()):
    ki[k] = [p for p in ki[k] if p <= max_pos]
    if not ki[k]:
        del ki[k]

# Re-add 30006/30007 keyword entries with correct positions
for pos, item in enumerate(new_items):
    bc = item.get('base_code','')
    if bc not in ('30006','30007'):
        continue
    vc = item.get('variant_code','').lower()
    keys_to_add = [
        bc, bc + vc,
        (bc + ' ' + vc).strip().replace(' ',''),
        'extendibleshowerhose', 'showerhose', 'hose'
    ]
    if bc == '30006':
        keys_to_add += ['1mtr', '1.0mtr']
    if bc == '30007':
        keys_to_add += ['1.5mtr', '15mtr']
    for k in keys_to_add:
        k = k.strip().lower()
        if not k: continue
        if k not in ki: ki[k] = []
        if pos not in ki[k]: ki[k].append(pos)

d['stored_items'] = new_items
d['keyword_index'] = ki

with open('search_index_v2.json','w',encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False)

print(f"\nVerify 30006 entries now:")
for i in new_items:
    if i.get('base_code','') in ('30006','30007'):
        print(f"  {i.get('search_code'):20} | {i.get('price'):6} | {i.get('name','')[:40]}")

print(f"\nSaved. Total items: {len(new_items)}")
