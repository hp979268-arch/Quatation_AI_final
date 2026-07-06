"""
CORRECT Aquant PDF Price Extraction

CONFIRMED FORMAT (by user):
  Line 1: "5141 BRG  5141 GG  5141 CP"
  Line 2: "5141 BG   5141 MB        MRP : 29,500/-"   <-- this is CP price
  Line 3: "Wall Mounted HydroGlide Shower..."
  Line 4: "Size : 265 x 225 mm  |  MRP : 39,500/-"   <-- this is SPECIAL FINISH price

So:
  - MRP on model listing line (with BG/MB) = CP price
  - MRP on Size line OR standalone MRP after description = Special finish price (BRG/BG/GG/MB/RG)
"""

import pdfplumber
import re
import json

PDF_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\uploads\Aquant Price List Vol 15. Feb 2026_Searchable.pdf'

TARGET_BASES = [
    '1314','1457','1459','1476','1477','1482',
    '2093','2096','2098','2113','2564',
    '2641','2642','2644','28118','28192','28194',
    '28201','28202','4006','4052',
    '5104','5105','5122','5123','5141',
    '1479','2101','2121','2561','2594','3166','4051',
    '2565','2646',
]

def extract_mrp(text):
    match = re.search(r'MRP\s*[:\s`\']+\s*([\d,]+)\s*/?\-?', text, re.IGNORECASE)
    if match:
        val = match.group(1).replace(',', '')
        try:
            v = int(val)
            if 100 <= v <= 9999999:
                return v
        except:
            pass
    return None

results = {}

print("Extracting with CORRECT logic from Aquant PDF...")
print("=" * 70)

with pdfplumber.open(PDF_PATH) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if not text:
            continue

        lines = text.split('\n')

        for i, line in enumerate(lines):
            line_clean = line.replace('\x00', ' ').strip()

            for base in TARGET_BASES:
                if base in results:
                    continue  # already found this base

                # Check if line has special finishes for this base
                has_special = bool(re.search(rf'\b{re.escape(base)}\s+(?:BRG|BG|GG|MB)\b', line_clean))
                if not has_special:
                    continue

                # Found a model listing line with special finishes
                # MRP on THIS line (or the next line that continues the listing) = CP price
                cp_mrp = None
                special_mrp = None

                # Search this line and next line for CP price (model line MRP)
                for j in range(i, min(i+2, len(lines))):
                    lj = lines[j].replace('\x00', ' ').strip()
                    # Model listing line MRP = CP price
                    mrp = extract_mrp(lj)
                    if mrp and cp_mrp is None:
                        # Only take if this line also has the base code (confirming it's still the model listing)
                        if base in lj:
                            cp_mrp = mrp

                # Search next 3 lines for special finish price
                # (description line then size/MRP line)
                for j in range(i+1, min(i+5, len(lines))):
                    lj = lines[j].replace('\x00', ' ').strip()

                    # Skip lines that still have model numbers
                    if re.search(rf'\b{re.escape(base)}\s+(?:BRG|BG|GG|MB|CP|RG)\b', lj):
                        mrp = extract_mrp(lj)
                        if mrp and cp_mrp is None:
                            cp_mrp = mrp
                        continue

                    # Size line or standalone MRP line = special finish price
                    mrp = extract_mrp(lj)
                    if mrp and special_mrp is None:
                        # Check it's not a model listing line for another product
                        # (no large base code present)
                        other_base = any(
                            re.search(rf'\b{re.escape(b)}\s+(?:BRG|BG|GG|MB|CP)\b', lj)
                            for b in TARGET_BASES if b != base
                        )
                        if not other_base:
                            special_mrp = mrp
                            break

                if special_mrp or cp_mrp:
                    results[base] = {
                        'special_finish_mrp': special_mrp,
                        'cp_mrp': cp_mrp,
                        'page': page_num,
                        'model_line': line_clean[:80]
                    }
                    sf = f"Rs.{special_mrp:,}" if special_mrp else "NOT FOUND"
                    cp = f"Rs.{cp_mrp:,}" if cp_mrp else "NOT FOUND"
                    print(f"  {base:8s} | CP={cp:18s} | Special={sf:18s} | pg.{page_num}")

print()
print("=" * 70)
found = len(results)
missing = [b for b in TARGET_BASES if b not in results]
print(f"Found: {found} / {len(TARGET_BASES)}")
if missing:
    print(f"Missing: {missing}")

out_path = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_prices_correct.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"Saved to: {out_path}")
