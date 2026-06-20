import pymongo
from pymongo import MongoClient
import os

OLD_URI = "mongodb+srv://admin:admin123@cluster0.5dxlcpj.mongodb.net/?appName=Cluster0"
NEW_URI = "mongodb+srv://hp979268_db_user:PQo6mPT7DugIoi4f@cluster0.wkcfszp.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "quotation_ai"

def migrate_database():
    try:
        print("Connecting to old MongoDB...")
        old_client = MongoClient(OLD_URI)
        old_db = old_client[DB_NAME]
        
        print("Connecting to new MongoDB...")
        new_client = MongoClient(NEW_URI)
        new_db = new_client[DB_NAME]
        
        collections = old_db.list_collection_names()
        print(f"Found collections to migrate: {collections}")
        
        for coll_name in collections:
            print(f"\nMigrating collection: {coll_name}...")
            old_coll = old_db[coll_name]
            new_coll = new_db[coll_name]
            
            # Clear new collection first (optional, but good for clean start)
            new_coll.delete_many({})
            
            docs = list(old_coll.find({}))
            if docs:
                new_coll.insert_many(docs)
                print(f"Successfully migrated {len(docs)} documents to '{coll_name}'.")
            else:
                print(f"Collection '{coll_name}' is empty.")
                
        print("\nDatabase migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_database()
