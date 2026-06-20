import shutil
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()
import mongodb

src_image = r"static\images\Kohler\K-22786IN-4-BV.png"
dst_image = r"static\images\Kohler\K-22786IN-4-BV_v7.png"

# Check if src image exists
if not os.path.exists(src_image):
    print(f"Error: {src_image} not found!")
    sys.exit(1)

# Copy the image to bust cache
shutil.copy2(src_image, dst_image)
print(f"Copied to {dst_image}")

# Update index
index_file = "search_index_v2.json"
with open(index_file, "r", encoding="utf-8") as f:
    db = json.load(f)

for item in db["stored_items"]:
    if "K-22786IN-4-BV" in item.get("search_code", ""):
        item["images"] = ["/static/images/Kohler/K-22786IN-4-BV_v7.png"]
        print(f"Updated index array for K-22786IN-4-BV")

with open(index_file, "w", encoding="utf-8") as f:
    json.dump(db, f)

print("Updated local search_index_v2.json")

# Update MongoDB
try:
    mongodb.save_search_index(db)
    print("Updated MongoDB search index!")
except Exception as e:
    print(f"Failed to update MongoDB: {e}")
