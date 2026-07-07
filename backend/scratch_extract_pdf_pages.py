import fitz

pdf_path = "c:/Movies/quotation-ai/quotation-ai/backend/uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
pages_to_check = [23, 24, 26, 30, 31, 52, 54, 59]

doc = fitz.open(pdf_path)

for p in pages_to_check:
    print(f"=== PAGE {p} ===")
    # Try p-1 because pdf pages are usually 0-indexed
    text = doc[p-1].get_text()
    lines = text.split('\n')
    for line in lines:
        if any(code in line for code in ["2592", "2562", "2569", "2104", "2106", "2102", "1411", "1415", "1418", "1320", "1437", "1155", "1485"]):
            print(f"[{p}] {line.strip()}")
            # Print a few lines after
            idx = lines.index(line)
            for i in range(1, 15):
                if idx + i < len(lines):
                    print(f"  + {lines[idx+i].strip()}")
            print("-" * 30)

doc.close()
