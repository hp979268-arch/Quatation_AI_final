import pdfplumber
import os

PDF_PATH = r"C:\Movies\quotation-ai\quotation-ai\backend\uploads\Kohler_PriceBook (June'26).pdf"

missing_codes = [
    '38519IN-0', '28786IN-0', '27792IN-0', '26994IN-HB1',
    '32989IN-NA', '97360T-B4-CP', '5584IN-0', '26995IN-2-0'
]

if os.path.exists(PDF_PATH):
    print('Found PDF')
    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
            for code in missing_codes:
                if code in text:
                    print(f'\nFound {code} on page {page_num}')
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if code in line:
                            start = max(0, i-1)
                            end = min(len(lines), i+3)
                            for j in range(start, end):
                                print(f'[{j+1}] {lines[j]}')
