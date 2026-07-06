"""
Simulate name-based search to verify it works for both Aquant and Kohler.
Uses the same logic as search_engine.py.
"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    d = json.load(f)
items = d['stored_items']
ki = d.get('keyword_index', {})

def simulate_search(query, brand_filter=None, top=5):
    query_lower = query.lower()
    query_words = [w for w in re.split(r'[\s\-\/]+', query_lower) if len(w) >= 2]
    
    # Get candidates via keyword index
    candidates = set()
    for w in query_words:
        if w in ki:
            candidates.update(ki[w])
    # Fallback: partial
    if not candidates:
        for k in ki:
            if any(w in k for w in query_words):
                candidates.update(ki[k])
    
    # Score
    scores = {}
    for idx in candidates:
        if idx >= len(items): continue
        item = items[idx]
        if brand_filter and item.get('brand','').lower() != brand_filter.lower():
            continue
        name_lower = item.get('name','').lower()
        text_lower = item.get('text','').lower()
        combined = name_lower + ' ' + text_lower
        s = 0
        if query_lower in name_lower: s += 380
        if query_lower in text_lower: s += 120
        for w in query_words:
            if w in combined: s += 45
            if w in name_lower: s += 35
        if query_words and all(w in combined for w in query_words): s += 140
        if s >= 100:
            scores[idx] = s
    
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return [(items[idx].get('search_code','?'), items[idx].get('name','?')[:45], items[idx].get('price','?'), round(score)) 
            for idx, score in ranked[:top]]

# Test cases
tests = [
    # Aquant
    ("basin mixer", "Aquant"),
    ("health faucet", "Aquant"),
    ("pillar cock", "Aquant"),
    ("bib cock", "Aquant"),
    ("angle valve", "Aquant"),
    ("bottle trap", "Aquant"),
    ("rain shower", "Aquant"),
    ("shower arm", "Aquant"),
    ("towel rod", "Aquant"),
    ("robe hook", "Aquant"),
    ("soap dish", "Aquant"),
    ("cistern", "Aquant"),
    ("aquabliss", "Aquant"),
    ("bidet attachment", "Aquant"),
    ("seat cover", "Aquant"),
    ("wash basin", "Aquant"),
    ("shower hose", "Aquant"),
    # Kohler
    ("bath", "Kohler"),
    ("shower", "Kohler"),
    ("lavatory faucet", "Kohler"),
    ("diverter", "Kohler"),
    ("bathtub", "Kohler"),
]

print("=== NAME SEARCH TEST ===\n")
ok = 0
fail = 0
for query, brand in tests:
    results = simulate_search(query, brand)
    status = "OK" if results else "FAIL - no results"
    if results: ok += 1
    else: fail += 1
    print(f"  [{brand}] '{query}' -> {status}")
    if results:
        for sc, name, price, score in results[:2]:
            print(f"    {sc:20} | {name} | Rs.{price}")
    print()

print(f"TOTAL: {ok} OK, {fail} FAILED")
