import urllib.request
import urllib.parse
import json

code = """
res = ""
for item in search_engine.stored_items:
    if item.get('search_code') == 'K-26297IN BL':
        img = search_engine._best_item_image(item)
        res += str(img) + ","
res
"""
url = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code.replace('\n', '\\n'))
try:
    print(urllib.request.urlopen(url).read().decode())
except Exception as e:
    print(e)
