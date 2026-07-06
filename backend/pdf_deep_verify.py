"""
Deep PDF price extractor for Aquant price list.
Uses page rendering + multiple text extraction modes to get MRP for each product code.
"""
import json, sys, io, re, fitz
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PDF_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\uploads\Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
items = data["stored_items"]

def find_base(b):
    return [i for i in items if i.get("base_code","").upper() == b.upper()]

doc = fitz.open(PDF_PATH)
print(f"PDF: {doc.page_count} pages\n")

def clean(text):
    """Remove control/special chars, normalize spaces."""
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def get_page_text(page_num_1indexed):
    pg = doc[page_num_1indexed - 1]
    # Try dict-based extraction for better accuracy
    blocks = pg.get_text("dict")["blocks"]
    lines_text = []
    for b in blocks:
        if b.get("type") == 0:  # text block
            for line in b.get("lines", []):
                line_str = " ".join(span["text"] for span in line.get("spans", []))
                line_str = clean(line_str).strip()
                if line_str:
                    lines_text.append(line_str)
    return "\n".join(lines_text)

def extract_prices_from_page(page_text, base_code, variant_codes=None):
    """
    Find prices for a given base_code on a page.
    Returns dict: variant_code -> price
    """
    results = {}
    lines = page_text.split('\n')
    
    # Find all price occurrences: look for patterns like 12,500/- or Rs 12500 or MRP : 12,500
    price_re = re.compile(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:/-|/-)?\s*(?=\s|$)')
    
    # Strategy: find the code line, then look for prices in the next 10 lines
    for i, line in enumerate(lines):
        # Check if this line contains our base code
        if re.search(r'\b' + re.escape(base_code) + r'\b', line, re.IGNORECASE):
            # Extract the variant from this line if present
            variant_match = re.search(
                r'\b' + re.escape(base_code) + r'\s*[-]?\s*([A-Z0-9]+)\b',
                line, re.IGNORECASE
            )
            variant = variant_match.group(1) if variant_match else ""
            
            # Look ahead for price
            context = "\n".join(lines[i:min(len(lines), i+12)])
            # Pattern 1: X,XXX/-
            prices_found = re.findall(r'(\d{1,3}(?:,\d{3})+)\s*/-', context)
            if not prices_found:
                # Pattern 2: MRP : X,XXX
                prices_found = re.findall(r'(?:MRP|Rs\.?)\s*:?\s*`?\s*([\d,]+)', context, re.IGNORECASE)
            if not prices_found:
                # Pattern 3: standalone numbers 4-6 digits
                prices_found = re.findall(r'\b(\d{4,6})\b', context)
            
            clean_prices = []
            for p in prices_found:
                try:
                    val = int(str(p).replace(',',''))
                    if 500 <= val <= 600000:
                        clean_prices.append(val)
                except:
                    pass
            
            key = (base_code + " " + variant).strip() if variant else base_code
            if clean_prices:
                results[key] = clean_prices
    
    return results

# ---- Products to check with their PDF pages ----
CHECKS = [
    # (base_code, page_list, note)
    ("30006", [20, 43], "30006/30007 G-Gold, 1.5m"),
    ("30007", [20, 43], "30006/30007"),
    ("2592",  [20], ""),
    ("2562",  [23], ""),
    ("2563",  [24], ""),
    ("3161",  [24], ""),
    ("3162",  [25], ""),
    ("3163",  [25], ""),
    ("2569",  [25, 26], ""),
    ("2122",  [26, 28], ""),
    ("2114",  [29], ""),
    ("2104",  [30], ""),
    ("2106",  [30], ""),
    ("2102",  [30, 31], ""),
    ("1411",  [31], ""),
    ("1415",  [31], ""),
    ("1418",  [31], ""),
    ("1419",  [31], ""),
    ("1507",  [91], "except BSS"),
    ("1501",  [91], ""),
    ("1025",  [90], "AquaBliss"),
    ("1506",  [90], ""),
    ("1947",  [86], ""),
    ("1936",  [85], "SM Statuario Matt"),
    ("1902",  [85], "SM Statuario Matt"),
    ("9057",  [66], "Konig"),
    ("1151",  [63], ""),
    ("1152",  [63], ""),
    ("1153",  [63], ""),
    ("1460",  [63], ""),
    ("1487",  [63], ""),
    ("1461",  [63], ""),
    ("1462",  [63], ""),
    ("1010",  [63], ""),
    ("28088", [61], ""),
    ("1318",  [59], ""),
    ("1319",  [59], ""),
    ("1320",  [59], "750BRG"),
    ("1436",  [59], ""),
    ("1437",  [59], "750BRG"),
    ("60080", [58], "BSCH"),
    ("90080", [58], "BSCH"),
    ("750080",[58], "BSCH"),
    ("1439",  [57], "Fleur"),
    ("1258",  [56], "Revive"),
    ("1256",  [56], "Eden"),
    ("1245",  [56], "Divine"),
    ("1257",  [56], "Retro"),
    ("1155",  [54], ""),
    ("28197", [54], ""),
    ("28198", [54], ""),
    ("1485",  [52], ""),
    ("2750",  [48], ""),
    ("2741",  [48], ""),
    ("2728",  [47], ""),
    ("2726",  [47], ""),
    ("2729",  [47], ""),
    ("2721",  [46], ""),
    ("1472",  [45], ""),
    ("2650",  [44], ""),
    ("7011",  [44], ""),
    ("1186",  [43], ""),
    ("1125",  [42], ""),
    ("1424",  [40], "200/500"),
]

out_lines = []
confirmed_mismatches = []
confirmed_missing = []
needs_manual = []

def hdr(t): out_lines.append(f"\n{'='*70}\n{t}\n{'='*70}")
def row(label, idx_p, pdf_prices, verdict): 
    out_lines.append(f"  {label:<28} | Idx={str(idx_p):<8} | PDF={str(pdf_prices):<22} | {verdict}")

for base_code, pages, note in CHECKS:
    label = base_code + (f" ({note})" if note else "")
    hdr(f"[{label}]  Pages: {pages}")
    
    index_items = find_base(base_code)
    
    # Collect page texts
    page_texts = {}
    for pg in pages:
        if 1 <= pg <= doc.page_count:
            page_texts[pg] = get_page_text(pg)
    
    combined_text = "\n".join(page_texts.values())
    
    # Show raw page text for manual checking
    out_lines.append(f"\n  -- RAW PAGE TEXT (pages {pages}) --")
    for pg, txt in page_texts.items():
        out_lines.append(f"  [Page {pg}]:")
        for line in txt.split('\n'):
            line = line.strip()
            if line and (base_code in line.upper() or 
                         'MRP' in line.upper() or 
                         re.search(r'\d{4,6}\s*/-', line) or
                         re.search(r'(?:BRG|BG|GG|MB|RG|CP|BSS|SM|BM)\b', line)):
                out_lines.append(f"    {line}")
    out_lines.append("  -- END RAW --")
    
    if not index_items:
        msg = f"  [!!] {base_code} NOT IN INDEX"
        out_lines.append(msg)
        confirmed_missing.append(base_code)
    else:
        # Compare index prices with PDF
        pdf_prices_found = extract_prices_from_page(combined_text, base_code)
        out_lines.append(f"\n  Index items vs PDF:")
        for item in index_items:
            sc = item.get("search_code","?")
            vc = item.get("variant_code","")
            idx_price = item.get("price","?")
            finish = item.get("finish_label","")[:18]
            
            # Get matching PDF price
            key1 = (base_code + " " + vc).strip()
            key2 = base_code
            pdf_p = pdf_prices_found.get(key1) or pdf_prices_found.get(key2) or []
            
            if pdf_p:
                idx_val = 0
                try: idx_val = int(str(idx_price).replace(',','').split('.')[0])
                except: pass
                if any(abs(p - idx_val) < 100 for p in pdf_p):
                    verdict = "[OK] Match"
                else:
                    verdict = f"[!!] MISMATCH"
                    confirmed_mismatches.append((sc, idx_price, pdf_p))
            else:
                verdict = "[??] Manual check needed"
                needs_manual.append((sc, idx_price))
            
            row(sc, idx_price, pdf_p if pdf_p else "not extracted", verdict)

# Summary
hdr("FINAL SUMMARY")
out_lines.append(f"\nCONFIRMED MISSING FROM INDEX ({len(confirmed_missing)}):")
for c in confirmed_missing:
    out_lines.append(f"  - {c}")

out_lines.append(f"\nCONFIRMED PRICE MISMATCHES ({len(confirmed_mismatches)}):")
for sc, idx, pdf in confirmed_mismatches:
    out_lines.append(f"  - {sc}: index={idx}, PDF suggests={pdf}")

out_lines.append(f"\nNEEDS MANUAL CHECK ({len(needs_manual)}):")
for sc, idx in needs_manual:
    out_lines.append(f"  - {sc}: index={idx}")

result = "\n".join(out_lines)
print(result)

out_path = r"c:\Movies\quotation-ai\quotation-ai\backend\pdf_deep_verify.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result)
print(f"\n[Saved to {out_path}]")
doc.close()
