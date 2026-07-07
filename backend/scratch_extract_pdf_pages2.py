import fitz

pdf_path = "c:/Movies/quotation-ai/quotation-ai/backend/uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
pages_to_check = [23, 24, 26, 30, 31, 52, 54, 59]
target_codes = ["2592", "2562", "2569", "2104", "2106", "2102", "1411", "1415", "1418", "1320", "1437", "1155", "1485"]

doc = fitz.open(pdf_path)

for p in pages_to_check:
    text = doc[p-1].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for i, line in enumerate(lines):
        if any(code in line for code in target_codes):
            print(f"[{p}] {line}")
            for j in range(1, 10):
                if i+j < len(lines):
                    if "MRP" in lines[i+j] or any(c in lines[i+j] for c in target_codes):
                        print(f"  + {lines[i+j]}")
                        if "MRP" in lines[i+j]:
                            break
            print("-" * 20)

doc.close()
