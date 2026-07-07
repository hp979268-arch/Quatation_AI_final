import json
import re

file_path = "c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json"
with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# Exact corrections as per client - {base_code: {variant: correct_price}}
CORRECTIONS = {
    "2592": {"GG": 35750, "MB": 35750, "RG": 35750},
    "2562": {"GG": 29500, "MB": 29500, "RG": 29500},
    "2569": {"GG": 145000, "MB": 145000, "RG": 145000},
    "2104": {"BRG": 42000, "GG": 42000, "RG": 42000, "BG": 42000, "MB": 42000},
    "2106": {"BRG": 59000, "GG": 59000, "RG": 59000, "BG": 59000, "MB": 59000},
    "2102": {"BRG": 24500, "GG": 24500, "RG": 24500, "BG": 24500, "MB": 24500},
    "1411": {"BRG": 6800, "GG": 6800, "RG": 6800, "BG": 6800, "MB": 6800},
    "1415": {"BRG": 8750, "GG": 8750, "RG": 8750, "BG": 8750, "MB": 8750},
    "1418": {"BRG": 6950, "GG": 6950, "RG": 6950, "BG": 6950, "MB": 6950},
    "1320-750": {"BRG": 17500, "GG": 17500, "BG": 17500, "MB": 17500},
    "1437-750": {"BRG": 17750, "GG": 17750, "BG": 17750, "MB": 17750},
}

BASE_CORRECTIONS = {
    "1155": 950,
    "1485": 8800,
}

items = data.get("stored_items", [])
updated = 0

for item in items:
    if item.get("brand") != "Aquant":
        continue

    base_code = str(item.get("base_code", ""))
    variant_code = str(item.get("variant_code", ""))
    search_code = str(item.get("search_code", item.get("name", "")))

    # Fix variant items (separate entries per variant)
    if base_code in CORRECTIONS and variant_code in CORRECTIONS[base_code]:
        correct_price = CORRECTIONS[base_code][variant_code]
        old_price = item.get("price")
        if str(old_price) != str(correct_price):
            print(f"  {search_code}: {old_price} -> {correct_price}")
            item["price"] = str(correct_price)
            updated += 1

    # Fix base items (1155, 1485)
    for code, correct_price in BASE_CORRECTIONS.items():
        if base_code == code or search_code == code or item.get("name", "") == code:
            old_price = item.get("price")
            if float(old_price) != float(correct_price):
                print(f"  {search_code}: {old_price} -> {correct_price}")
                item["price"] = str(correct_price)
                updated += 1

if updated > 0:
    # Bump cache version
    data["version"] = data.get("version", 1) + 1
    for item in items:
        new_images = []
        for img in item.get("images", []):
            if "?v=" in img:
                base, rest = img.split("?v=", 1)
                v_num = int(rest.split("&")[0]) if rest.split("&")[0].isdigit() else 1
                new_images.append(f"{base}?v={v_num+1}")
            else:
                new_images.append(img)
        item["images"] = new_images

    with open(file_path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, indent=4)
    print(f"\nDone! Updated {updated} prices. Cache version: {data['version']}")
else:
    print("No prices needed updating.")
