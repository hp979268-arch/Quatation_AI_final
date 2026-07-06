"""
PDF Price Verifier - Extracts MRP from Aquant PDF for all reported products
and compares with search_index_v2.json prices.
READ ONLY - no changes made.
"""
import json, sys, io, re, fitz
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PDF_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\uploads\Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
items = data["stored_items"]

def find_base(b):
    b = b.upper()
    return [i for i in items if i.get("base_code","").upper() == b]

# Pages to check (0-indexed so subtract 1)
# user reported these pages:
REPORTED = {
    "30006/30007": [19, 42],   # pg 20, 43
    "2592": [19],
    "2562": [22],
    "2563": [23],
    "3161": [23],
    "3162": [24],
    "3163": [24],
    "2569": [24, 25],
    "2122": [25, 27],
    "2114": [28],
    "2104": [29],
    "2106": [29],
    "2102": [29, 30],
    "1411": [30],
    "1415": [30],
    "1418": [30],
    "1419": [30],
    "1507": [30, 90],
    "1501": [90],
    "1506": [89],
    "1947": [85],
    "1936": [84],
    "1902": [84],
    "9057": [65, 76],
    "1151": [62],
    "1152": [62],
    "1153": [62],
    "1460": [62],
    "1487": [62],
    "1461": [62],
    "1462": [62],
    "1010": [62],
    "28088": [60],
    "1318": [58],
    "1319": [58],
    "1320": [58],
    "1436": [58],
    "1437": [58],
    "60080": [57],
    "90080": [57],
    "750080": [57],
    "1439": [56],
    "1258": [55],
    "1256": [55],
    "1245": [55],
    "1257": [55],
    "1155": [53],
    "28197": [53],
    "28198": [53],
    "1485": [51],
    "2750": [47],
    "2741": [47],
    "2728": [46],
    "2726": [46],
    "2729": [46],
    "2721": [45],
    "1472": [44],
    "2650": [43],
    "7011": [43],
    "1186": [42],
    "1125": [41],
    "1424": [39],
    "1025": [89],
    "1803": [0],  # seat covers - will search all
    "1821": [0],
}

doc = fitz.open(PDF_PATH)
total_pages = doc.page_count
print(f"PDF loaded: {total_pages} pages\n")

def extract_page_text(page_num_0indexed):
    if page_num_0indexed < 0 or page_num_0indexed >= total_pages:
        return ""
    return doc[page_num_0indexed].get_text()

def find_price_in_text(text, code):
    """Find MRP/price near a product code in text."""
    prices = []
    # Find all ₹ or Rs prices
    price_patterns = [
        r'(?:MRP|Rs\.?|₹)\s*:?\s*([\d,]+(?:\.\d+)?)',
        r'([\d,]+)/-',
        r'\b(\d{3,6})\b'
    ]
    # Look for code then nearby price
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if code in line.upper():
            # Check surrounding lines for price
            context = '\n'.join(lines[max(0,i-2):min(len(lines),i+5)])
            for pat in price_patterns[:2]:
                found = re.findall(pat, context, re.IGNORECASE)
                for p in found:
                    val = int(p.replace(',','').split('.')[0])
                    if 500 <= val <= 500000:
                        prices.append(val)
    return list(set(prices))

out = []
def sec(t): out.append(f"\n{'='*65}\n  {t}\n{'='*65}")
def row(c, idx_p, pdf_p, status):
    out.append(f"  {c:<25} | Index: {str(idx_p):<10} | PDF: {str(pdf_p):<20} | {status}")

sec("HEADER: Code | Index Price | PDF Extracted Price | Status")

for base_code, pages in REPORTED.items():
    sec(f"Product: {base_code}  (PDF pages: {[p+1 for p in pages if p > 0]})")
    
    # Get index items
    index_items = find_base(base_code)
    
    # Collect PDF text from relevant pages
    pdf_text = ""
    for pg in pages:
        if pg > 0:
            pdf_text += extract_page_text(pg - 1)  # convert to 0-index
    
    # If no pages specified or pg=0, do a search across all pages
    if not any(p > 0 for p in pages) or base_code in ["1803","1821"]:
        for pg_num in range(total_pages):
            t = extract_page_text(pg_num)
            if base_code in t:
                pdf_text += f"\n[PAGE {pg_num+1}]\n" + t
    
    # Extract prices from PDF text near code
    pdf_prices = find_price_in_text(pdf_text, base_code)
    
    if not index_items:
        out.append(f"  [!!] NOT IN INDEX at all!")
        if pdf_prices:
            out.append(f"  [--] PDF prices found: {pdf_prices}")
        else:
            out.append(f"  [--] No prices found in PDF either for this code")
    else:
        for item in index_items:
            sc = item.get("search_code","")
            variant = item.get("variant_code","")
            idx_price = item.get("price","?")
            finish = item.get("finish_label","")
            
            # Try to find variant-specific price in PDF
            v_prices = find_price_in_text(pdf_text, (base_code + " " + variant).strip())
            final_pdf = v_prices if v_prices else pdf_prices
            
            if final_pdf:
                idx_val = int(str(idx_price).replace(',','').split('.')[0]) if idx_price else 0
                if any(abs(p - idx_val) < 50 for p in final_pdf):
                    status = "[OK] Match"
                else:
                    status = f"[!!] MISMATCH - verify manually"
            else:
                status = "[??] PDF price not auto-extracted"
            
            row(f"{sc} ({finish[:15]})", idx_price, final_pdf if final_pdf else "N/A", status)

    # Also show raw PDF text snippet around the code for manual verification
    if pdf_text:
        lines = pdf_text.split('\n')
        snippet_lines = []
        for i, line in enumerate(lines):
            if base_code in line.upper() or base_code.replace("/"," ") in line.upper():
                snippet_lines.extend(lines[max(0,i-1):min(len(lines),i+6)])
        if snippet_lines:
            out.append(f"\n  --- PDF TEXT SNIPPET ---")
            for sl in snippet_lines[:20]:
                sl = sl.strip()
                if sl:
                    out.append(f"  | {sl}")
            out.append(f"  ------------------------")

# --- IMAGE CHECK ---
sec("IMAGE CHECK: Missing images for reported products")
import os
IMAGE_DIR = r"c:\Movies\quotation-ai\quotation-ai\backend\static\images\Aquant"
existing_images = set(os.listdir(IMAGE_DIR)) if os.path.exists(IMAGE_DIR) else set()

all_reported_bases = list(REPORTED.keys())
missing_images = []
for base in all_reported_bases:
    its = find_base(base)
    for item in its:
        imgs = item.get("images", [])
        if not imgs:
            missing_images.append((item.get("search_code","?"), "NO IMAGE URL in index"))
        else:
            for img_url in imgs:
                # Extract filename
                fname = img_url.split("/")[-1].split("?")[0]
                if fname and fname not in existing_images:
                    missing_images.append((item.get("search_code","?"), f"FILE MISSING: {fname}"))

if missing_images:
    out.append(f"  Total missing images: {len(missing_images)}")
    for sc, issue in missing_images:
        out.append(f"  [!!] {sc:<25} | {issue}")
else:
    out.append("  [OK] All image files present for reported products")

result = "\n".join(out)
print(result)

out_path = r"c:\Movies\quotation-ai\quotation-ai\backend\pdf_price_verify_output.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result)
print(f"\n[Saved to {out_path}]")
doc.close()
