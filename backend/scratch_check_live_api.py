import urllib.request
import json

res = urllib.request.urlopen('https://quotation-ai-backend-dn5t.onrender.com/search-suggestions?q=750080+TL').read().decode()
data = json.loads(res)
print(json.dumps(data, indent=2)[:2000])
