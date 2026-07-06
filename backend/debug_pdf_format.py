import pdfplumber

PDF_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\uploads\Aquant Price List Vol 15. Feb 2026_Searchable.pdf'

target_bases = ['5141', '4051', '1314', '2641', '28118']

with pdfplumber.open(PDF_PATH) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    
    for page_num, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if not text:
            continue
        
        for base in target_bases:
            if base in text:
                print(f"\n{'='*60}")
                print(f"Found '{base}' on PAGE {page_num}")
                print(f"{'='*60}")
                # Print surrounding lines
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if base in line:
                        start = max(0, i-1)
                        end = min(len(lines), i+6)
                        print(f"  Context (lines {start+1}-{end}):")
                        for j in range(start, end):
                            print(f"    [{j+1}] {lines[j]}")
                        print()
                        break  # just first occurrence per page
