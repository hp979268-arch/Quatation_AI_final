"""
Verify product name search works for both Aquant and Kohler.
Check keyword_index has proper name-based keys.
"""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    d = json.load(f)
items = d['stored_items']
ki = d.get('keyword_index', {})

# Test: search for common product name keywords - check if they exist in keyword_index
test_searches = [
    # Aquant product names
    "basin mixer", "health faucet", "shower hose", "bidet",
    "pillar cock", "bib cock", "angle valve", "bottle trap",
    "rain shower", "shower arm", "towel rod", "robe hook",
    "toilet roll", "soap dish", "napkin holder", "seat cover",
    "wash basin", "shower panel", "cistern", "aquabliss",
    # Kohler product names  
    "bath", "trim", "valve", "faucet", "mixer", "diverter",
    "shower", "spout", "tub", "lavatory"
]

print("=== KEYWORD INDEX NAME SEARCH TEST ===\n")
missing_keys = []
found_keys = []
for term in test_searches:
    clean = term.lower().replace(" ","")
    # Check if term or cleaned version is in keyword_index
    hits = ki.get(term.lower(), []) or ki.get(clean, [])
    if hits:
        found_keys.append((term, len(hits)))
    else:
        missing_keys.append(term)

print(f"Found ({len(found_keys)}):")
for t, c in found_keys:
    print(f"  '{t}' -> {c} results")

print(f"\nMissing ({len(missing_keys)}) - these wont show in name search:")
for t in missing_keys:
    print(f"  '{t}'")

# Count how many items have NO name-based keywords indexed
print("\n=== ITEMS WITH INSUFFICIENT NAME INDEXING ===")
aquant_sample = [i for i in items if i.get('brand')=='Aquant'][:10]
kohler_sample = [i for i in items if i.get('brand')=='Kohler'][:10]

def get_name_words(item):
    name = item.get('name','').lower()
    name = re.sub(r'[^a-z0-9 ]', ' ', name)
    return [w for w in name.split() if len(w) >= 3]

# Check a few
for item in aquant_sample[:5]:
    words = get_name_words(item)
    indexed = [w for w in words if any(w in k for k in ki)]
    print(f"  {item.get('search_code','?'):20} | words={words[:4]} | indexed={indexed[:3]}")
