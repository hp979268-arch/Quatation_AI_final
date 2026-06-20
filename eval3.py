import urllib.request
import urllib.parse

code = "search_engine._resolved_code_to_image_cache.get('K-30318IN', 'NOT FOUND')"
url = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code)
try:
    print(urllib.request.urlopen(url).read().decode())
except Exception as e:
    print(e)
