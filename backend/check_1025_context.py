import fitz, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
doc = fitz.open(r'uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf')
page = doc[89]  # page 90
blocks = page.get_text('dict')['blocks']
lines = []
for b in blocks:
    if b.get('type') == 0:
        for line in b.get('lines',[]):
            t = ' '.join(s['text'] for s in line.get('spans',[])).strip()
            if t: lines.append(t)
# Show lines around 1025
for i, l in enumerate(lines):
    if '1025' in l:
        context = lines[max(0,i-3):i+8]
        for c in context: print(c)
        break
doc.close()
