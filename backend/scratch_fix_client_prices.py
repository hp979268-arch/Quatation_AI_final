import json

file_path = "c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json"
with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

corrections = {
    "2592": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 46750},
    "2562": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 36750},
    "2569": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 117000},
    "2104": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 59000},
    "2106": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 65000},
    "2102": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 29250},
    "1411": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 8750},
    "1415": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 6950},
    "1418": {"variants": ["BRG", "BG", "GG", "MB", "RG"], "price": 8250},
}

base_corrections = {
    "1155": 950,
    "1485": 8800,
    "1320-750 BRG": 7000,
    "1320-750 BG": 7000,
    "1320-750 GG": 7000,
    "1320-750 MB": 7000,
    "1437-750 BRG": 4750,
    "1437-750 BG": 4750,
    "1437-750 GG": 4750,
    "1437-750 MB": 4750,
}

items = data.get("stored_items", [])
updated_count = 0

for item in items:
    if item.get("brand") != "Aquant":
        continue
        
    base_code = item.get("base_code")
    search_code = item.get("search_code", item.get("name"))
    
    if base_code in corrections:
        correct_price = corrections[base_code]["price"]
        target_variants = corrections[base_code]["variants"]
        
        if item.get("variant_code") in target_variants:
            if float(item.get("price")) != float(correct_price):
                print(f"Updating {search_code} from {item.get('price')} to {correct_price}")
                item["price"] = str(correct_price)
                updated_count += 1
                
        variants = item.get("variants", [])
        for v in variants:
            v_code = v.get("code", "")
            for tv in target_variants:
                if v_code == tv or v_code.endswith(" " + tv):
                    if float(v.get("price", 0)) != float(correct_price):
                        print(f"Updating variant array item {v_code} under {base_code} to {correct_price}")
                        v["price"] = str(correct_price)
                        updated_count += 1

    for k, v in base_corrections.items():
        if search_code == k or item.get("name") == k:
            if float(item.get("price")) != float(v):
                print(f"Updating base item {search_code} from {item.get('price')} to {v}")
                item["price"] = str(v)
                updated_count += 1
        
        for var in item.get("variants", []):
            if var.get("code", "") == k or var.get("name", "") == k:
                if float(var.get("price", 0)) != float(v):
                    print(f"Updating base variant {k} under {search_code} to {v}")
                    var["price"] = str(v)
                    updated_count += 1

if updated_count > 0:
    with open(file_path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully updated {updated_count} prices!")
else:
    print("No prices needed updating.")
