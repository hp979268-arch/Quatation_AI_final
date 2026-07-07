import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import search_engine

def main():
    search_engine.load_index(force=True)
    
    print("--- Searching '1850W' ---")
    res = search_engine.search("1850W")
    print(f"Results: {len(res)}")
    for r in res[:10]:
        print(f"- {r.get('name')} | {r.get('search_code')}")
        
    print("\n--- Searching 'extra' ---")
    res2 = search_engine.search("extra")
    print(f"Results: {len(res2)}")
    for r in res2[:10]:
        print(f"- {r.get('name')} | {r.get('search_code')}")
        
if __name__ == "__main__":
    main()
