import json
import fitz

# 1. Check Current JSON Prices
print("=== CURRENT JSON PRICES ===")
file_path = "c:/Movies/quotation-ai/quotation-ai/backend/search_index_v2.json"
with open(file_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

target_codes = ["30006", "30007", "1125", "1424-500", "1424-200"]

for item in data.get("stored_items", []):
    if item.get("brand") != "Aquant": continue
    sc = str(item.get("search_code", item.get("name")))
    bc = str(item.get("base_code", ""))
    
    if any(t in sc or t == bc for t in target_codes):
        print(f"{sc} : {item.get('price')} (variant array: {len(item.get('variants', []))})")
        for v in item.get('variants', []):
            print(f"  - {v.get('code', v.get('name'))} : {v.get('price')}")
            
print("\n=== PDF EXTRACTED PRICES ===")
pdf_path = "c:/Movies/quotation-ai/quotation-ai/backend/uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
pages_to_check = [40, 42, 43]
doc = fitz.open(pdf_path)

for p in pages_to_check:
    print(f"\n[PAGE {p}]")
    text = doc[p-1].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for i, line in enumerate(lines):
        if any(c in line for c in target_codes):
            print(f"-> {line}")
            for j in range(1, 8):
                if i+j < len(lines):
                    print(f"    {lines[i+j]}")
                    if "MRP" in lines[i+j] or any(c in lines[i+j] for c in target_codes):
                        break

doc.close()
