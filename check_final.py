import json, re

path = r'C:\Users\DELL\.gemini\antigravity\brain\61d699f3-b1fd-424e-b82d-d67a8ec98b77\.system_generated\steps\543\content.md'
text = open(path, encoding='utf-8').read()
match = re.search(r'\{"suggestions.*', text)
if match:
    data = json.loads(match.group())
    s = data.get('suggestions', [])
    print(f'=== 30520 search === ({len(s)} results)')
    for r in s:
        ri = r.get('raw_item') or {}
        print(f'  Code: {r.get("display_code")} | Price: {r.get("price")} | Image: {ri.get("images")}')
else:
    print('No match found in response')
    print(text[:500])
