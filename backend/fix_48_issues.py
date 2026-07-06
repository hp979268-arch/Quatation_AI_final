import json
import time

def fix_all_issues():
    index_path = 'search_index_v2.json'
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    items = data.get('stored_items', [])
    new_items = []
    
    price_fixes = {
        "2709": "3950",
        "2722": "5750",
        "2724": "2950",
        "2742": "6000",
        "2744": "3950",
        "2747": "3950",
        "2749": "3750",
        "1446": "2600",
        "1505": "15250",
        "2708": "3950"
    }
    
    delete_special_for = ["1017", "1186", "1419"]
    special_finishes = ["BRG", "BG", "GG", "MB", "RG"]
    
    deleted_count = 0
    updated_count = 0
    
    for item in items:
        if item.get('brand') == 'Aquant':
            base_code = item.get('base_code', '')
            v_code = item.get('variant_code', '')
            
            # Delete injected special finishes
            if base_code in delete_special_for and v_code in special_finishes:
                deleted_count += 1
                continue
                
            # Update correct special finishes
            if base_code in price_fixes and v_code in special_finishes:
                if item.get('price') != price_fixes[base_code]:
                    item['price'] = price_fixes[base_code]
                    item['mrp'] = price_fixes[base_code]
                    updated_count += 1
                    
        new_items.append(item)
        
    data['stored_items'] = new_items
    
    if updated_count > 0 or deleted_count > 0:
        data['version'] = str(int(time.time()))
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {updated_count} products.")
        print(f"Deleted {deleted_count} invalid products.")
    else:
        print("No changes needed.")

if __name__ == '__main__':
    fix_all_issues()
