import fitz

doc = fitz.open('backend/uploads/Kohler_PriceBook (June\'26).pdf')
for i, page in enumerate(doc):
    text = page.get_text()
    if '30520' in text:
        print(f"--- PAGE {i} ---")
        lines = text.split('\n')
        for idx, line in enumerate(lines):
            if '30520' in line or '13100' in line or '11800' in line or '10000' in line:
                start = max(0, idx - 2)
                end = min(len(lines), idx + 3)
                print('\n'.join(lines[start:end]))
                print('---')
