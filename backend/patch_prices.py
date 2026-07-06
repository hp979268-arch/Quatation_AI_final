import json
import shutil
import time

def patch_prices():
    index_path = 'search_index_v2.json'
    backup_path = f'search_index_v2_backup_{int(time.time())}.json'
    
    # Backup
    shutil.copy(index_path, backup_path)
    
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    price_fixes = {
        "2591": "27500",
        "2593": "46750",
        "2566": "6400",
        "3162": "18950",
        "3163": "7450",
        "2102": "29250",
        "1411": "8750",
        "1415": "6950",
        "1456": "2350",
        "1449": "4200",
        "2645": "8500"
    }
    
    special_finishes = ["BRG", "BG", "GG", "MB", "RG"]
    
    items = data.get('stored_items', [])
    updated_count = 0
    
    for product in items:
        if product.get('brand') == 'Aquant':
            base_code = product.get('base_code', '')
            v_code = product.get('variant_code', '')
            
            if base_code in price_fixes and v_code in special_finishes:
                correct_price = price_fixes[base_code]
                if product.get('price') != correct_price:
                    name = product.get('name', f"{base_code} {v_code}")
                    print(f"Updating {name} from {product['price']} to {correct_price}")
                    product['price'] = correct_price
                    product['mrp'] = correct_price
                    # update text
                    if product.get('text'):
                        product['text'] = product['text'].replace(product.get('price', ''), correct_price)
                    updated_count += 1
    
    if updated_count > 0:
        # Bump version to bust cache on frontend
        if 'version' in data:
            data['version'] = str(int(time.time()))
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {updated_count} products.")
    else:
        print("No products needed updating.")

if __name__ == '__main__':
    patch_prices()
