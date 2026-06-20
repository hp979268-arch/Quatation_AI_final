import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()
import mongodb

index_file = "search_index_v2.json"
with open(index_file, "r", encoding="utf-8") as f:
    db = json.load(f)

for item in db["stored_items"]:
    code = item.get("search_code", "")
    if code == "K-22786IN-4-BV":
        item["images"] = ["/static/images/Kohler/k22786_bv_ok.png"]
    elif code == "K-22786IN-4-RGD":
        item["images"] = ["/static/images/Kohler/k22786_rgd_ok.png"]
    elif code == "K-22786IN-4-BRD":
        item["images"] = ["/static/images/Kohler/k22786_brd_ok.png"]

with open(index_file, "w", encoding="utf-8") as f:
    json.dump(db, f)

print("Updated search_index_v2.json")

try:
    mongodb.save_search_index(db)
    print("Updated MongoDB search index!")
except Exception as e:
    print("Failed to update MongoDB:", e)
    sys.exit(1)
