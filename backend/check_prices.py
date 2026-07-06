import json

def check_prices():
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('stored_items', [])
    skus_to_check = [
        "2591", "2593", "2566", "3162", "3163", "2102", "1411", "1415", "1456", "1449", "2645"
    ]
    
    res = {}
    for product in items:
        if product.get('brand') == 'Aquant':
            base_code = product.get('base_code', '')
            if base_code in skus_to_check:
                if base_code not in res:
                    res[base_code] = {}
                res[base_code][product.get('variant_code')] = product.get('price')
    
    for sku in skus_to_check:
        print(f"{sku}: {res.get(sku, 'Not found')}")

if __name__ == '__main__':
    check_prices()
