import json

file_path = "c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json"
target_codes = ["2592", "2562", "2569", "2104", "2106", "2102", "1411", "1415", "1418", "1320", "1437", "1155", "1485"]

with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)
    
items = data.get("stored_items", [])

for item in items:
    id_str = str(item.get("id", ""))
    name_str = str(item.get("name", ""))
    
    match = False
    for code in target_codes:
        if code in id_str or code in name_str:
            match = True
            break
            
    if match and item.get("brand") == "AQUANT":
        print(f"ID: {item.get('id')} | Name: {item.get('name')}")
        variants = item.get("variants", [])
        if variants:
            for v in variants:
                print(f"  - Variant {v.get('code', v.get('name'))}: Rs {v.get('price')}")
        else:
            print(f"  - Base Price: Rs {item.get('price')}")
        print("-" * 50)
