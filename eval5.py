import urllib.request
import urllib.parse
import json

code = """
def trace_it():
    res = []
    for item in search_engine.stored_items:
        if '30318IN BL' in str(item.get('search_code', '')):
            res.append(search_engine._best_item_image(item))
    return res
trace_it()
"""

url = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code.replace('\n', '\\n'))
try:
    print(urllib.request.urlopen(url).read().decode())
except Exception as e:
    print(e)
