import fitz
import os

pdf_path = "uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
if not os.path.exists(pdf_path):
    pdf_path = "backend/uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"

doc = fitz.open(pdf_path)
page = doc[87] # Page 88 is index 87
print("--- Page 88 text ---")
for b in page.get_text("blocks"):
    print(b)
