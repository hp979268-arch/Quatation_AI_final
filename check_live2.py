import json, re

files = {
    '30520 (after refresh)': r'C:\Users\DELL\.gemini\antigravity\brain\61d699f3-b1fd-424e-b82d-d67a8ec98b77\.system_generated\steps\489\content.md',
}

def extract_suggestions(path):
    text = open(path, encoding='utf-8').read()
    match = re.search(r'\{"suggestions.*', text)
    if not match: return []
    try:
        data = json.loads(match.group())
        return [(s.get('display_code') or s.get('text'), s.get('price'), (s.get('raw_item') or {}).get('images', [])) for s in data.get('suggestions', [])]
    except Exception as e:
        return [('ERROR', str(e), [])]

for code, path in files.items():
    s = extract_suggestions(path)
    print(f'=== {code} === ({len(s)} results)')
    for r in s:
        print(f'  Code: {r[0]} | Price: {r[1]} | Image: {r[2]}')
