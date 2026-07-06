import json

with open('c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data.get('stored_items', [])

variants_1003 = {
    'CP':  {'label': 'Chrome Plated', 'price': '2950'},
    'G':   {'label': 'Gold',          'price': '7500'},
    'BRG': {'label': 'Brushed Rose Gold', 'price': '7500'},
    'BG':  {'label': 'Brushed Gold',  'price': '7500'},
    'GG':  {'label': 'Graphite Grey', 'price': '7500'},
    'MB':  {'label': 'Matt Black',    'price': '7500'},
    'RG':  {'label': 'Rose Gold',     'price': '7500'},
    'AB':  {'label': 'Antique Bronze','price': '7500'},
}

variants_450 = {
    'CP':  {'label': 'Chrome Plated', 'price': '2100'},
    'G':   {'label': 'Gold',          'price': '3250'},
    'BRG': {'label': 'Brushed Rose Gold', 'price': '3250'},
    'BG':  {'label': 'Brushed Gold',  'price': '3250'},
    'GG':  {'label': 'Graphite Grey', 'price': '3250'},
    'MB':  {'label': 'Matt Black',    'price': '3250'},
    'RG':  {'label': 'Rose Gold',     'price': '3250'},
}

# Find a template
template = next((i for i in items if i.get('brand') == 'Aquant' and i.get('page') == 19), None)

new_entries = []

# Process 1003
for finish, info in variants_1003.items():
    code = f"1003 {finish}"
    desc = f"Brass Bottle Trap - {info['label']}\nSize : 32 mm With 300 mm Long Pipe\nMRP : ₹ {info['price']}/-"
    entry = {
        "text": f"1003 {finish}\n{code} - {desc}",
        "name": f"{code} - Brass Bottle Trap - {info['label']}",
        "price": info['price'],
        "page": 42,
        "source": template['source'] if template else "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": [f"/static/images/Aquant/1003 {finish}.png"],
        "brand": "Aquant",
        "category": "ALLIED PRODUCTS" if finish != 'AB' else "Stellar Series- Antique Bronze",
        "base_code": "1003",
        "variant_code": finish,
        "full_code": code,
        "search_code": code,
        "finish_label": info['label']
    }
    new_entries.append(entry)

# Process 450-1003
for finish, info in variants_450.items():
    code = f"450-1003 {finish}"
    desc = f"Bottle Trap Pipe - {info['label']}\nSize : 450 mm\nMRP : ₹ {info['price']}/-"
    entry = {
        "text": f"450-1003 {finish}\n{code} - {desc}",
        "name": f"{code} - Bottle Trap Pipe - {info['label']}",
        "price": info['price'],
        "page": 42,
        "source": template['source'] if template else "Aquant Price List Vol 15. Feb 2026_Searchable",
        "images": [f"/static/images/Aquant/450-1003 {finish}.png"],
        "brand": "Aquant",
        "category": "ALLIED PRODUCTS",
        "base_code": "450-1003",
        "variant_code": finish,
        "full_code": code,
        "search_code": code,
        "finish_label": info['label']
    }
    new_entries.append(entry)

# Remove old items for 1003 and 450-1003
items_cleaned = []
for i in items:
    s_code = i.get('search_code', '')
    if s_code.startswith('1003 ') or s_code.startswith('450-1003 '):
        continue
    items_cleaned.append(i)

items_cleaned.extend(new_entries)
data['stored_items'] = items_cleaned

with open('c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    
print(f"Added {len(new_entries)} entries for 1003 and 450-1003.")
