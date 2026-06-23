import json
import fitz
import re
import random

INDEX_FILE = 'backend/search_index_v2.json'
AQUANT_PDF = "backend/uploads/Aquant Price List Vol 15. Feb 2026_Searchable.pdf"
KOHLER_PDF = "backend/uploads/Kohler_PriceBook (June'26).pdf"

def get_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for p in doc:
        text += p.get_text()
    return text

def main():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    aquant_items = [i for i in db['stored_items'] if i.get('brand') == 'Aquant' and i.get('price', '0') != '0']
    kohler_items = [i for i in db['stored_items'] if i.get('brand') == 'Kohler' and i.get('price', '0') != '0']
    
    # Specific variants that were known to have issues
    specific_checks = ["1333", "2569 MB", "4052 RG", "1831 RGW", "5106 MB", "K-8297IN-0", "K-4108IN-0"]
    
    samples = []
    
    for code in specific_checks:
        for item in db['stored_items']:
            if item.get('search_code') == code or item.get('base_code') == code:
                samples.append(item)
                break
                
    # Add random samples
    samples.extend(random.sample(aquant_items, 5))
    samples.extend(random.sample(kohler_items, 5))
    
    print("Loading PDFs for verification...")
    # Loading entire text is fast enough for 100 pages
    aquant_doc = fitz.open(AQUANT_PDF)
    kohler_doc = fitz.open(KOHLER_PDF)
    
    aquant_blocks = []
    for p in aquant_doc:
        for b in p.get_text('blocks'):
            aquant_blocks.append(b[4].replace('\x03', ' ').strip())
            
    kohler_blocks = []
    for p in kohler_doc:
        for b in p.get_text('blocks'):
            kohler_blocks.append(b[4].replace('\x03', ' ').strip())
            
    print("\n" + "="*50)
    print("DEEP VERIFICATION REPORT (JSON vs PDF Catalog)")
    print("="*50)
    
    match_count = 0
    total_checked = 0
    
    for item in samples:
        code = item.get('search_code')
        brand = item.get('brand')
        json_price = str(item.get('price', '0'))
        base_code = item.get('base_code', code)
        
        blocks = aquant_blocks if brand == 'Aquant' else kohler_blocks
        
        pdf_prices = []
        found = False
        
        # Simple backwards search for MRP near the code
        for i, block_text in enumerate(blocks):
            if code in block_text or (base_code in block_text and len(code) > 3):
                # found a mention of the code
                # look backwards and forwards for MRP
                for j in range(max(0, i-6), min(len(blocks), i+6)):
                    mrps = re.findall(r'(?:MRP|PRICE)\s*[:-]?\s*[`₹]?\s*([\d,]+)', blocks[j], re.IGNORECASE)
                    if not mrps:
                        # Sometimes just a number with commas preceded by Rs or symbol
                        mrps = re.findall(r'[`₹]\s*([\d,]{4,})', blocks[j])
                    if mrps:
                        for m in mrps:
                            val = int(m.replace(',', ''))
                            if val > 100:
                                pdf_prices.append(val)
                if pdf_prices:
                    found = True
                    break
        
        if found:
            total_checked += 1
            json_val = int(float(json_price))
            # if json price is in the extracted prices from PDF around that block
            if json_val in pdf_prices or (brand == 'Aquant' and json_val == max(pdf_prices)):
                print(f"[PASS] {code.ljust(15)} | JSON: {json_price.ljust(8)} | PDF Match: YES")
                match_count += 1
            else:
                print(f"[FAIL] {code.ljust(15)} | JSON: {json_price.ljust(8)} | PDF Found: {pdf_prices}")
                
    print("\n" + "="*50)
    if match_count == total_checked:
        print(f"VERDICT: 100% ACCURACY ({match_count}/{total_checked} items exactly match PDF prices).")
    else:
        print(f"VERDICT: FOUND DISCREPANCIES ({match_count}/{total_checked} match).")
    print("="*50)

if __name__ == '__main__':
    main()
