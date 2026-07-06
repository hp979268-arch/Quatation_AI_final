import fitz, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
doc = fitz.open(r'uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf')
# Check pages 89-91 for 1025
for pg_num in [88, 89, 90]:
    page = doc[pg_num]
    blocks = page.get_text('dict')['blocks']
    lines = []
    for b in blocks:
        if b.get('type') == 0:
            for line in b.get('lines',[]):
                t = ' '.join(s['text'] for s in line.get('spans',[])).strip()
                if t and ('1025' in t or 'AquaBliss' in t or 'Aqua' in t.lower() or 'Bidet' in t or 'bidet' in t.lower()):
                    lines.append(f"  [pg{pg_num+1}] {t}")
    for l in lines: print(l)
doc.close()
