"""
Extract clean page text for manual price verification.
Saves per-page readable text for all reported pages.
"""
import fitz, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PDF_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\uploads\Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
doc = fitz.open(PDF_PATH)

PAGES_TO_CHECK = sorted(set([
    20, 23, 24, 25, 26, 28, 29, 30, 31,
    40, 42, 43, 44, 45, 46, 47, 48,
    52, 54, 56, 57, 58, 59, 61, 63, 66,
    85, 86, 90, 91
]))

out = []
for pg_num in PAGES_TO_CHECK:
    if pg_num < 1 or pg_num > doc.page_count:
        continue
    page = doc[pg_num - 1]
    # Use blocks for cleaner extraction
    blocks = page.get_text("dict")["blocks"]
    page_lines = []
    for b in blocks:
        if b.get("type") == 0:
            for line in b.get("lines", []):
                spans_text = " ".join(s["text"] for s in line.get("spans", []))
                spans_text = spans_text.strip()
                if spans_text:
                    page_lines.append(spans_text)
    
    out.append(f"\n{'#'*60}")
    out.append(f"# PAGE {pg_num}")
    out.append(f"{'#'*60}")
    out.extend(page_lines)

result = "\n".join(out)
out_path = r"c:\Movies\quotation-ai\quotation-ai\backend\pages_for_manual_check.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result)
print(f"Saved {len(PAGES_TO_CHECK)} pages to {out_path}")
doc.close()
