import fitz

pdf_path = "uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
query = "73050"

print(f"Opening PDF: {pdf_path}")
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
matches = []

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text()
    if query in text:
        matches.append((page_num + 1, text))

print(f"\nFound {len(matches)} pages containing '{query}':")
for page_no, text in matches:
    print(f"--- Page {page_no} ---")
    lines = text.split("\n")
    for line in lines:
        if query in line:
            print(line)
