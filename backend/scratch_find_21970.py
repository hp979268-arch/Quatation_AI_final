import fitz
for pdf in [r"backend/uploads/Aquant Sanitaryware MRP.pdf", r"backend/uploads/Aquant Showering MRP.pdf"]:
    doc = fitz.open(pdf)
    for p in doc:
        if '2748' in p.get_text():
            print(f"Code 2748 is on page {p.number} in {pdf}")
