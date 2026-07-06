import fitz  # PyMuPDF

def search_pdf():
    pdf_path = "uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
    targets = ["2591", "2593", "2566", "3162", "3163", "2102", "1411", "1415", "1456", "1449", "2645"]
    
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        text = page.get_text()
        if not text:
            continue
        
        found = [t for t in targets if t in text]
        if found:
            print(f"--- Page {i+1} ---")
            lines = text.split('\n')
            for j, line in enumerate(lines):
                if any(t in line for t in found):
                    start = max(0, j-10)
                    end = min(len(lines), j+10)
                    print(f"Match for {found} at line {j}:")
                    print('\n'.join(lines[start:end]))
                    print("-----------------")

if __name__ == '__main__':
    search_pdf()
