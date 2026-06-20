import urllib.request
import urllib.parse
import json

code = "search_engine.keyword_index.get('faucet cleaner', 'NOT FOUND')"
url = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code)
try:
    print(urllib.request.urlopen(url).read().decode())
except Exception as e:
    print(e)
