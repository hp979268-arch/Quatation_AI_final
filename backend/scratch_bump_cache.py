import json
import re

file_path = "c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json"
with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# Increment global version
current_v = data.get("version", 1)
data["version"] = current_v + 1
print(f"Bumped JSON version to {data['version']}")

# Bump image cache strings
items = data.get("stored_items", [])
updated = 0
for item in items:
    images = item.get("images", [])
    new_images = []
    for img in images:
        if "?" in img:
            base, query = img.split("?", 1)
            if "v=" in query:
                v_num = int(re.search(r'v=(\d+)', query).group(1))
                new_img = f"{base}?v={v_num+1}"
            else:
                new_img = f"{img}&v=2"
        else:
            new_img = f"{img}?v=2"
        if new_img != img:
            new_images.append(new_img)
            updated += 1
        else:
            new_images.append(img)
    item["images"] = new_images

if updated > 0:
    with open(file_path, "w", encoding="utf-8-sig") as f:
        json.dump(data, f, indent=4)
    print(f"Updated {updated} image cache versions.")
else:
    print("No images needed cache update.")
