import json
import fitz
import os

def fix_274_images():
    doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
    
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    codes_to_fix = [i for i in db['stored_items'] if i.get('search_code', '').startswith('K-274')]
    
    # We need to find the page and Y coordinate for each code
    # We can scan the PDF once
    code_locations = {}
    for p in doc:
        for b in p.get_text('blocks'):
            text = b[4]
            # Some codes might have spaces or newlines
            for item in codes_to_fix:
                code = item['search_code']
                # match K-27482IN-4ND-CP
                # in PDF it might be K-27482IN-4ND-CP or K-27482IN-4ND CP
                pdf_code_1 = code
                pdf_code_2 = code.replace('-', ' ')
                
                if pdf_code_1 in text or pdf_code_2 in text:
                    code_locations[code] = (p.number, b[1], b[3]) # page, y0, y1
                    
    print(f"Found {len(code_locations)} locations out of {len(codes_to_fix)} codes.")
    
    os.makedirs('backend/static/images/Kohler', exist_ok=True)
    changed = 0
    
    for item in codes_to_fix:
        code = item['search_code']
        if code in code_locations:
            pnum, y0, y1 = code_locations[code]
            p = doc[pnum]
            
            y_above = y0 - 30
            y_below = y1 + 50
            
            # Use X=30 to 85 to isolate the left item
            rect = fitz.Rect(30, y_above, 90, y_below)
            pix = p.get_pixmap(clip=rect, dpi=300)
            os.makedirs('static/images/Kohler', exist_ok=True)
            new_img_name = f"/static/images/Kohler/{code}_v5.png"
            new_img_path = "." + new_img_name
            pix.save(new_img_path)
            
            item['images'] = [new_img_name]
            changed += 1
            print(f"Fixed {code}")
            
    if changed > 0:
        with open('search_index_v2.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        from mongodb import get_db
        mongo = get_db()
        if mongo is not None:
            mongo.search_index_v2.replace_one({}, db, upsert=True)
            print("MongoDB updated.")
            
if __name__ == '__main__':
    fix_274_images()
