import json
import os

def audit_catalog():
    with open('backend/search_index_v2.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    kohler_items = [i for i in db['stored_items'] if i.get('brand') == 'Kohler']
    aquant_items = [i for i in db['stored_items'] if i.get('brand') == 'Aquant']

    report = []
    
    # 1. Price Checks
    kohler_zero = [i for i in kohler_items if not i.get('price') or str(i.get('price')) == '0']
    aquant_zero = [i for i in aquant_items if not i.get('price') or str(i.get('price')) == '0']
    
    kohler_low = [i for i in kohler_items if str(i.get('price', '0')).isdigit() and int(i.get('price', '0')) > 0 and int(i.get('price', '0')) < 500]
    aquant_low = [i for i in aquant_items if str(i.get('price', '0')).isdigit() and int(i.get('price', '0')) > 0 and int(i.get('price', '0')) < 500]

    report.append(f"--- KOHLER PRICE AUDIT ---")
    report.append(f"Zero Price: {len(kohler_zero)}")
    if kohler_zero: report.append(f"Examples: {[i['search_code'] for i in kohler_zero[:5]]}")
    report.append(f"Low Price (<500): {len(kohler_low)}")
    if kohler_low: report.append(f"Examples: {[(i['search_code'], i['price']) for i in kohler_low[:5]]}")

    report.append(f"\n--- AQUANT PRICE AUDIT ---")
    report.append(f"Zero Price: {len(aquant_zero)}")
    if aquant_zero: report.append(f"Examples: {[i['search_code'] for i in aquant_zero[:5]]}")
    report.append(f"Low Price (<500): {len(aquant_low)}")
    if aquant_low: report.append(f"Examples: {[(i['search_code'], i['price']) for i in aquant_low[:5]]}")

    # 2. Image Checks
    kohler_no_img = [i for i in kohler_items if not i.get('images') or not i['images'][0]]
    aquant_no_img = [i for i in aquant_items if not i.get('images') or not i['images'][0]]
    
    report.append(f"\n--- KOHLER IMAGE AUDIT ---")
    report.append(f"No Image: {len(kohler_no_img)}")
    if kohler_no_img: report.append(f"Examples: {[i['search_code'] for i in kohler_no_img[:5]]}")
    
    # Check for missing files on disk
    missing_disk_kohler = []
    for i in kohler_items:
        if i.get('images') and i['images'][0]:
            path = 'backend' + i['images'][0]
            if not os.path.exists(path):
                missing_disk_kohler.append(i['search_code'])
    report.append(f"Image File Missing on Disk: {len(missing_disk_kohler)}")
    if missing_disk_kohler: report.append(f"Examples: {missing_disk_kohler[:5]}")

    report.append(f"\n--- AQUANT IMAGE AUDIT ---")
    report.append(f"No Image: {len(aquant_no_img)}")
    if aquant_no_img: report.append(f"Examples: {[i['search_code'] for i in aquant_no_img[:5]]}")
    
    missing_disk_aquant = []
    for i in aquant_items:
        if i.get('images') and i['images'][0]:
            path = 'backend' + i['images'][0]
            if not os.path.exists(path):
                missing_disk_aquant.append(i['search_code'])
    report.append(f"Image File Missing on Disk: {len(missing_disk_aquant)}")
    if missing_disk_aquant: report.append(f"Examples: {missing_disk_aquant[:5]}")

    with open('backend/audit_report.txt', 'w') as f:
        f.write('\n'.join(report))
        
    print("Audit complete.")

if __name__ == '__main__':
    audit_catalog()
