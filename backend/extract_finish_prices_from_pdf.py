"""
Aquant PDF Price Extractor - Special Finish Products
Format understanding:
  Line: "5141 BRG - Brushed Rose Gold  5141 GG - Graphite Grey  5141 CP"
  Next: "5141 BG - Brushed Gold  5141 MB - Matt Black        MRP : ` 29,500/-"
  Then: "Wall Mounted HydroGlide Shower..."
  Then: "Size : 265 x 225 mm   |   MRP : ` 39,500/-"

So: MRP on model line = special finish price (BRG/BG/GG/MB)
    MRP on size line = CP price (and sometimes RG has separate price)
    RG sometimes listed separately with its own MRP
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
    """Extract MRP value from text like 'MRP : ` 29,500/-' or 'MRP : Rs. 29500'"""
    # Match MRP followed by number
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

results = {}  # {base: {'special_finish_mrp': X, 'cp_mrp': Y, 'rg_mrp': Z, 'page': N}}

print("Extracting prices from Aquant PDF...")
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
                # Check if this line has the base code with special finish codes
                # Pattern: "XXXX BRG" or "XXXX GG" etc on the line
                has_special = bool(re.search(rf'\b{re.escape(base)}\s+(?:BRG|BG|GG|MB)\b', line_clean))
                
                if not has_special:
                    continue
                
                # Also check if RG is on this same line (sometimes it is)
                has_rg = bool(re.search(rf'\b{re.escape(base)}\s+RG\b', line_clean))
                
                # The SPECIAL FINISH MRP is usually on:
                # - Current line (if "MRP" appears here), OR
                # - Next line (the line with BG/MB and MRP at end)
                special_mrp = None
                cp_mrp = None
                rg_mrp = None
                
                # Check current + next 3 lines for MRP pattern
                for j in range(i, min(i+4, len(lines))):
                    line_j = lines[j].replace('\x00', ' ').strip()
                    mrp = extract_mrp(line_j)
                    
                    if mrp is None:
                        continue
                    
                    # Determine which MRP this is:
                    # If line has "Size" keyword -> CP/standard price
                    # If line has base code with MB/BG -> special finish price
                    # If line is just MRP (description line) -> special finish price
                    
                    if 'Size' in line_j or 'size' in line_j:
                        # This is CP price (size line)
                        if cp_mrp is None:
                            cp_mrp = mrp
                    elif base in line_j and re.search(rf'\b{re.escape(base)}\s+(?:BG|MB)\b', line_j):
                        # Line with BG/MB and MRP = special finish price
                        if special_mrp is None:
                            special_mrp = mrp
                    elif base in line_j and re.search(rf'\b{re.escape(base)}\s+RG\b', line_j):
                        # RG specific line
                        if rg_mrp is None:
                            rg_mrp = mrp
                    elif special_mrp is None and cp_mrp is None:
                        # Plain MRP line (description after model listing)
                        special_mrp = mrp
                
                if special_mrp or cp_mrp:
                    if base not in results:
                        results[base] = {
                            'special_finish_mrp': special_mrp,  # BRG, BG, GG, MB price
                            'cp_mrp': cp_mrp,
                            'rg_mrp': rg_mrp,
                            'page': page_num
                        }
                        # Print what we found
                        sf = f"Rs.{special_mrp:,}" if special_mrp else "N/A"
                        cp = f"Rs.{cp_mrp:,}" if cp_mrp else "N/A"
                        rg = f"Rs.{rg_mrp:,}" if rg_mrp else "N/A"
                        print(f"  {base:8s} | Special={sf:15s} | CP={cp:15s} | RG={rg} | pg.{page_num}")

print()
print("=" * 70)
print(f"Found: {len(results)} / {len(TARGET_BASES)} target products")

# Check which ones are missing
missing = [b for b in TARGET_BASES if b not in results]
if missing:
    print(f"Missing: {missing}")

# Save
out_path = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_prices_from_pdf.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\nSaved to: {out_path}")
