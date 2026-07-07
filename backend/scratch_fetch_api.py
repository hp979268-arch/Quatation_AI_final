import urllib.request
import re

url = "https://shreejiceramica.vercel.app/static/js/main.e5ee3062.js"
print(f"Fetching {url}...")
try:
    js = urllib.request.urlopen(url).read().decode('utf-8')
    urls = re.findall(r'https?://[^\s"\'`\}]+', js)
    unique_urls = set(urls)
    print("Found URLs in JS bundle:")
    for u in unique_urls:
        if 'react' not in u and 'w3.org' not in u and 'localhost' not in u and '127.0.0.1' not in u:
            print("-", u)
except Exception as e:
    print("Error:", e)
