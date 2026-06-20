import urllib.request
import urllib.parse
import json

code = "'faucet cleaner' in search_engine._keyword_keys_sorted"
url = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code)
try:
    print(urllib.request.urlopen(url).read().decode())
except Exception as e:
    print(e)

code2 = "'faucet cleaner' in search_engine.keyword_index"
url2 = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code2)
try:
    print(urllib.request.urlopen(url2).read().decode())
except Exception as e:
    print(e)
