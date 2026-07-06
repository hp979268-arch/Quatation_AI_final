import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('search_index_v2.json','r',encoding='utf-8') as f:
    d = json.load(f)
items = d['stored_items']

for item in items:
    if item.get('base_code','') == '1025':
        old_name = item.get('name','')
        # Update name to include AquaBliss
        item['name'] = '1025 - AquaBliss Bidet Attachment'
        item['text'] = '1025 - AquaBliss Bidet Attachment\nToilet Seat Attachment For Built-In Jet Spray'
        item['price'] = '4200'  # confirmed correct
        print(f"Updated: {old_name} -> {item['name']}")
        print(f"Price: {item['price']} - CONFIRMED OK")

with open('search_index_v2.json','w',encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False)
print("Saved.")
