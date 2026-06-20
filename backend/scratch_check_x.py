import fitz
import json
import os

pdf_path = r"backend/uploads/Kohler_PriceBook (June'26).pdf"
doc = fitz.open(pdf_path)

db = json.load(open('backend/search_index_v2.json', encoding='utf-8'))
codes = [i['search_code'] for i in db['stored_items'] if 'trim + valve' in i.get('text', '').lower() or 'trim + valve' in i.get('name', '').lower()]
codes = list(set(codes))

data = []
for code in codes:
    for p in doc:
        for b in p.get_text('blocks'):
            if code in b[4]:
                data.append((code, p.number, b[0], b[1], b[2], b[3]))

print(f"Found {len(data)} block matches.")
print("X coordinates:")
for d in data:
    print(f"Code: {d[0]}, Page: {d[1]}, X0: {d[2]}, Y0: {d[3]}, X1: {d[4]}, Y1: {d[5]}")
