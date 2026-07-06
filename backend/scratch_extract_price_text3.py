import fitz  # PyMuPDF
import re

def search_pdf():
    pdf_path = "uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
    targets = ["1017", "1419", "1446", "1186", "2708", "2709", "2722", "2724", "2742", "2744", "2747", "2749", "1505"]
    
    with open('output3.txt', 'w', encoding='utf-8') as out_f:
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            text = page.get_text()
            if not text:
                continue
            
            found = [t for t in targets if re.search(rf'\b{t}\b', text)]
            if found:
                out_f.write(f"--- Page {i+1} ---\n")
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    if any(re.search(rf'\b{t}\b', line) for t in found):
                        start = max(0, j-10)
                        end = min(len(lines), j+10)
                        out_f.write(f"Match for {found} at line {j}:\n")
                        out_f.write('\n'.join(lines[start:end]) + '\n')
                        out_f.write("-----------------\n")

if __name__ == '__main__':
    search_pdf()
