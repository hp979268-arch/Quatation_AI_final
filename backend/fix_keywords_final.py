import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    d = json.load(f)
items = d['stored_items']
ki = d.get('keyword_index', {})

# Fix 1: Add 'cistern' keyword for 1501, 1506 and any item with cistern in name/text
# Fix 2: Add 'aquabliss' keyword for 1025
# Fix 3: Enrich keyword index for common Aquant terms

EXTRA_KEYWORDS = {
    'cistern': ['1501','1506','1507'],
    'aquabliss': ['1025'],
    'pneumatic': ['1501','1506'],
    'flush plate': ['1507'],
    'flushplate': ['1507'],
}

added = 0
for keyword, base_codes in EXTRA_KEYWORDS.items():
    for pos, item in enumerate(items):
        bc = item.get('base_code','')
        if bc in base_codes:
            if keyword not in ki: ki[keyword] = []
            if pos not in ki[keyword]:
                ki[keyword].append(pos)
                added += 1

# Also: ensure 'aquabliss' points to 1025
for pos, item in enumerate(items):
    name = item.get('name','').lower()
    text = item.get('text','').lower()
    # Add 'cistern' for any item whose text mentions cistern
    if 'cistern' in name or 'cistern' in text:
        if 'cistern' not in ki: ki['cistern'] = []
        if pos not in ki['cistern']:
            ki['cistern'].append(pos)
            added += 1
    # Add 'aquabliss' 
    if 'aquabliss' in name or 'aquabliss' in text or item.get('base_code','') == '1025':
        if 'aquabliss' not in ki: ki['aquabliss'] = []
        if pos not in ki['aquabliss']:
            ki['aquabliss'].append(pos)
            added += 1

print(f"Added {added} keyword entries")
print(f"  cistern -> {len(ki.get('cistern',[]))} items")
print(f"  aquabliss -> {len(ki.get('aquabliss',[]))} items")

d['keyword_index'] = ki
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)
print("Saved.")
