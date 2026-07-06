
import json
import collections

data = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
items = data.get('stored_items', [])

duplicate_search_codes = collections.defaultdict(list)
for i, item in enumerate(items):
    if not isinstance(item, dict): continue
    sc = item.get('search_code')
    if sc:
        duplicate_search_codes[sc].append(item)

dupes = {k: v for k, v in duplicate_search_codes.items() if len(v) > 1}
for k, v in dupes.items():
    prices = [str(x.get('price')) for x in v]
    print(f'- **{k}**: Prices = {', '.join(prices)}')

