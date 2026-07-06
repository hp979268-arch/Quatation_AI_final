import fitz  # PyMuPDF
import re

def search_pdf():
    pdf_path = "uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
    targets = ["2591", "2593", "2566", "3162", "3163", "2102", "1411", "1415", "1456", "1449", "2645"]
    
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        text = page.get_text()
        if not text:
            continue
        
        found = [t for t in targets if re.search(rf'\b{t}\b', text)]
        if found:
            print(f"--- Page {i+1} ---")
            lines = text.split('\n')
            for j, line in enumerate(lines):
                if any(re.search(rf'\b{t}\b', line) for t in found):
                    start = max(0, j-5)
                    end = min(len(lines), j+8)
                    print(f"Match for {found} at line {j}:")
                    print('\n'.join(lines[start:end]))
                    print("-----------------")

if __name__ == '__main__':
    search_pdf()
