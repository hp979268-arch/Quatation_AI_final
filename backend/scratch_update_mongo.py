import json
import mongodb

index_file = "search_index_v2.json"
with open(index_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Updating MongoDB with latest search index...")
try:
    mongodb.save_search_index(data)
    print("Successfully updated MongoDB search index!")
except Exception as e:
    print(f"Failed to update MongoDB: {e}")
