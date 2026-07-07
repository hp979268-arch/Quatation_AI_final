import json
import pymongo
import os

MONGO_URI = "mongodb+srv://hp979268_db_user:PQo6mPT7DugIoi4f@cluster0.wkcfszp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("Connecting to MongoDB...")
client = pymongo.MongoClient(MONGO_URI)
db = client["quotation_ai"]

print("Fetching from MongoDB search_index_v3...")
doc = db["search_index_v3"].find_one({"_id": "global"})
if doc:
    items = doc.get("stored_items", [])
    query = "73050"
    matches = []
    for item in items:
        code = str(item.get("base_code") or "")
        search_code = str(item.get("search_code") or "")
        if query in code or query in search_code:
            matches.append(item)
    print(f"Found {len(matches)} matches in MongoDB:")
    for item in matches:
        print(f"Brand: {item.get('brand')} | SearchCode: {item.get('search_code')} | Name: {item.get('name')} | Price: {item.get('price')}")
else:
    print("No global document found in MongoDB.")
