import os
import json
from dotenv import load_dotenv
import pymongo

load_dotenv()

MONGO_URI = "mongodb+srv://admin:admin123@cluster0.5dxlcpj.mongodb.net/?appName=Cluster0"
INDEX_FILE = "backend/search_index_v2.json"

def main():
    if not MONGO_URI:
        print("MONGO_URI is not set.")
        return

    print("Loading local JSON...")
    with open(INDEX_FILE, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data.get('stored_items', []))} items from {INDEX_FILE}.")

    print("Connecting to MongoDB...")
    client = pymongo.MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
    db = client["quotation_ai"]
    
    print("Uploading to MongoDB...")
    doc = dict(data)
    doc["_id"] = "global"
    db["search_index"].replace_one({"_id": "global"}, doc, upsert=True)
    
    # Also sync to search_index_v2 collection if it exists, just in case
    db["search_index_v2"].replace_one({"_id": "global"}, doc, upsert=True)
    
    print("Successfully pushed latest search index to MongoDB!")

if __name__ == "__main__":
    main()
