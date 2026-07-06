import json

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'

new_items = [
  {
    "name": "K-38519IN-0 - Veil wall hung toilet with PureWash E910 electronic bidet seat cover (K-28362IN-2-0) with remote, in white",
    "price": "195000",
    "search_code": "K-38519IN-0",
    "base_code": "K-38519IN",
    "variant_code": "0",
    "finish_label": "White",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-38519IN-0.png"]
  },
  {
    "name": "K-28786IN-0 - Veil wall hung toilet with C3-230 electronic bidet seat cover (K-4108IN-0) with remote, in white",
    "price": "161000",
    "search_code": "K-28786IN-0",
    "base_code": "K-28786IN",
    "variant_code": "0",
    "finish_label": "White",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-28786IN-0.png"]
  },
  {
    "name": "K-27792IN-0 - ModernLife Edge wall hung toilet with Purewash E-880 electronic bidet seat cover (K-32387IN-0) with remote, in white",
    "price": "121000",
    "search_code": "K-27792IN-0",
    "base_code": "K-27792IN",
    "variant_code": "0",
    "finish_label": "White",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-27792IN-0.png"]
  },
  {
    "name": "K-26994IN-HB1 - Rimless wall hung toilet with Quiet-Close UF seat cover in honed black",
    "price": "50000",
    "search_code": "K-26994IN-HB1",
    "base_code": "K-26994IN",
    "variant_code": "HB1",
    "finish_label": "Honed Black",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-26994IN-HB1.png"]
  },
  {
    "name": "32989IN-NA - Kitchen sinks",
    "price": "2000",
    "search_code": "32989IN-NA",
    "base_code": "32989IN",
    "variant_code": "NA",
    "finish_label": "NA",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/32989IN-NA.png"]
  },
  {
    "name": "K-97360T-B4-CP - Deck-mount bath tub filler with hand shower in polished chrome",
    "price": "100000",
    "search_code": "K-97360T-B4-CP",
    "base_code": "K-97360T-B4",
    "variant_code": "CP",
    "finish_label": "Polished Chrome",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-97360T-B4-CP.png"]
  },
  {
    "name": "K-5584IN-0 - BRIVE+ Pedestal in white",
    "price": "5000",
    "search_code": "K-5584IN-0",
    "base_code": "K-5584IN",
    "variant_code": "0",
    "finish_label": "White",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-5584IN-0.png"]
  },
  {
    "name": "K-26995IN-2-0 - Brazn wall hung toilet with PureWash E910 electronic bidet seat cover (K-28820IN-0) with remote, in white",
    "price": "191000",
    "search_code": "K-26995IN-2-0",
    "base_code": "K-26995IN-2",
    "variant_code": "0",
    "finish_label": "White",
    "brand": "Kohler",
    "images": ["/static/images/Kohler/K-26995IN-2-0.png"]
  }
]

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data['stored_items']
existing_codes = {p['search_code'] for p in products}

added = 0
for item in new_items:
    if item['search_code'] not in existing_codes:
        products.append(item)
        added += 1
        print(f"Added {item['search_code']}")
    else:
        print(f"Skipped {item['search_code']} - already exists")

if added > 0:
    data['version'] = data.get('version', 1) + 1
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"Successfully added {added} items and bumped version to {data['version']}")
