import pdfplumber
import json

PDF_PATH = r"C:\Movies\quotation-ai\quotation-ai\backend\uploads\Kohler_PriceBook (June'26).pdf"
INDEX_PATH = r"C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"

codes_to_check = ['38896IN-4FS-BV', '30520IN-0']

# Check PDF
print('--- PDF Prices ---')
with pdfplumber.open(PDF_PATH) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if not text: continue
        for code in codes_to_check:
            if code in text:
                print(f'\nFound {code} on page {page_num}:')
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if code in line:
                        start = max(0, i-1)
                        end = min(len(lines), i+3)
                        for j in range(start, end):
                            print(f'  [{j+1}] {lines[j]}')

# Check Index
print('\n--- Search Index Prices ---')
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

for code in codes_to_check:
    full_code = 'K-' + code
    found = False
    for p in data['stored_items']:
        if p.get('search_code') == full_code or p.get('base_code') == full_code:
            print(f"Index: {full_code} | Price: {p.get('price')} | Name: {p.get('name')}")
            found = True
    if not found:
        print(f"Index: {full_code} | NOT FOUND in index")
