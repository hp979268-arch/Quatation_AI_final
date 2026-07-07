import fitz

pdf_path = "uploads/Kohler_PriceBook (June'26).pdf"
doc = fitz.open(pdf_path)

page = doc.load_page(96)  # 0-indexed page 96 is Page 97
print(page.get_text())
