import sys, os, json
sys.path.insert(0, os.path.abspath('.'))
import search_engine
search_engine.load_index(force=True)
found = None
for item in search_engine.stored_items:
    if item.get('search_code') == '750080 TL':
        found = item
        break
print('FOUND' if found else 'NOT FOUND')
if found:
    print(json.dumps(found, indent=2))
