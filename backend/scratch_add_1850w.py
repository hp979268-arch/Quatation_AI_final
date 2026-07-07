import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine
import mongodb

def main():
    items_to_add = [
        {
            "text": "Extra - Intelligent Toilet Seat\nMRP : ₹ 170000.00/-\nCompatible with 1850 W - SmartElite",
            "name": "Intelligent Toilet Seat (For 1850 W - SmartElite)",
            "price": "170000",
            "images": [
                "/static/images/Aquant/Intelligent Toilet Seat(1850W).png"
            ],
            "brand": "Aquant",
            "category": "INTELLIGENT SMART TOILET AQUANEXX SERIES",
            "base_code": "Intelligent Toilet Seat",
            "search_code": "Extra Intelligent Toilet Seat (1850 W)",
            "source": "Aquant Price List Vol 15. Feb 2026_Searchable"
        },
        {
            "text": "Extra - Intelligent Toilet Remote\nMRP : ₹ 9500.00/-\nCompatible with 1850 W - SmartElite",
            "name": "Intelligent Toilet Remote (For 1850 W - SmartElite)",
            "price": "9500",
            "images": [
                "/static/images/Aquant/Intelligent Toilet Remote(1850W).png"
            ],
            "brand": "Aquant",
            "category": "INTELLIGENT SMART TOILET AQUANEXX SERIES",
            "base_code": "Intelligent Toilet Remote",
            "search_code": "Extra Intelligent Toilet Remote (1850 W)",
            "source": "Aquant Price List Vol 15. Feb 2026_Searchable"
        },
        {
            "text": "Extra - Doorbell Remote\nMRP : ₹ 7500.00/-\nCompatible with 1850 W - SmartElite",
            "name": "Doorbell Remote (For 1850 W - SmartElite)",
            "price": "7500",
            "images": [
                "/static/images/Aquant/Doorbell Remote(1850W).png"
            ],
            "brand": "Aquant",
            "category": "INTELLIGENT SMART TOILET AQUANEXX SERIES",
            "base_code": "Doorbell Remote",
            "search_code": "Extra Doorbell Remote (1850 W)",
            "source": "Aquant Price List Vol 15. Feb 2026_Searchable"
        }
    ]

    print("Loading search index from MongoDB...")
    search_engine.load_index(force=True)
    
    print(f"Adding {len(items_to_add)} items to search engine...")
    search_engine.add_to_index(None, items_to_add)
    
    if mongodb.is_enabled():
        print("Pushing updated index to MongoDB Cloud...")
        data = {
            "stored_items": search_engine.stored_items,
            "keyword_index": search_engine.keyword_index
        }
        mongodb.save_search_index(data)
        print("Successfully synced to MongoDB!")
    else:
        print("Warning: MongoDB is not enabled.")

if __name__ == "__main__":
    main()
