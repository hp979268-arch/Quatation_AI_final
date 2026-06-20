import urllib.request
import urllib.parse

code = "search_engine._resolve_local_image_path('K-30318IN.png')"
url = 'http://localhost:8000/eval?code=' + urllib.parse.quote(code)
try:
    print(urllib.request.urlopen(url).read().decode())
except Exception as e:
    print(e)
