import json
import time
import subprocess
import os

INDEX_PATH = "search_index_v2.json"

print(f"Loading {INDEX_PATH}...")
with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

items = data.get("stored_items", [])
target_code = "K-73050T-B7-AF"

# Check if already exists
existing = [item for item in items if item.get("search_code") == target_code]
if existing:
    print(f"Product {target_code} already exists in database!")
    # Update price just in case
    for item in existing:
        item["price"] = "57800.00"
        item["text"] = "K-73050T-B7-AF - Single-control basin faucet with drain in french gold\nMRP : \u20b9 57800.00/-"
else:
    new_item = {
      "text": "K-73050T-B7-AF - Single-control basin faucet with drain in french gold\nMRP : \u20b9 57800.00/-",
      "name": "K-73050T-B7-AF - Single-control basin faucet with drain in french gold",
      "price": "57800.00",
      "images": [
        "/static/images/Kohler/K-73050T-B7-AF.png?v=39"
      ],
      "brand": "Kohler",
      "category": "French Gold",
      "search_code": "K-73050T-B7-AF",
      "base_code": "K-73050T-B7",
      "source": "Kohler_PriceBook (June'26)"
    }
    items.append(new_item)
    print(f"Added new product {target_code} to index.")

# Bump cache buster version
data["version"] = str(int(time.time()))

# Write back to index
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved updated index locally.")

# Execute mongo push script
print("Running direct_mongo_push.py...")
res = subprocess.run([r"..\.venv\Scripts\python.exe", "direct_mongo_push.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
