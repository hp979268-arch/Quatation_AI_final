import json, re

files = {
    '30520': r'C:\Users\DELL\.gemini\antigravity\brain\61d699f3-b1fd-424e-b82d-d67a8ec98b77\.system_generated\steps\469\content.md',
    '1021': r'C:\Users\DELL\.gemini\antigravity\brain\61d699f3-b1fd-424e-b82d-d67a8ec98b77\.system_generated\steps\470\content.md',
    '1017': r'C:\Users\DELL\.gemini\antigravity\brain\61d699f3-b1fd-424e-b82d-d67a8ec98b77\.system_generated\steps\471\content.md',
}

def extract_suggestions(path):
    text = open(path, encoding='utf-8').read()
    match = re.search(r'\{"suggestions.*', text)
    if not match: return []
    try:
        data = json.loads(match.group())
        return [(s.get('display_code') or s.get('text'), s.get('price')) for s in data.get('suggestions', [])]
    except Exception as e:
        return [('ERROR', str(e))]

for code, path in files.items():
    s = extract_suggestions(path)
    print(f'=== {code} === ({len(s)} results)')
    for r in s:
        print(f'  {r[0]} | Price: {r[1]}')
