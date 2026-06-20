import fitz
import os
import re
import json
from dotenv import load_dotenv
load_dotenv()
import mongodb

def extract_by_drawing(pdf_path):
    doc = fitz.open(pdf_path)
    output_dir = r"static\images\Kohler"
    
    extracted = []
    
    for page_num, page in enumerate(doc):
        blocks = page.get_text('blocks')
        drawings = page.get_drawings()
        
        h_lines = []
        for d in drawings:
            for item in d["items"]:
                if item[0] == "l":
                    p1, p2 = item[1], item[2]
                    if abs(p1.y - p2.y) < 1:
                        h_lines.append(p1.y)
                        
        h_lines.sort()
        
        for b in blocks:
            text = b[4].lower()
            if "trim + valve" in text or "trim & valve" in text:
                match = re.search(r'K-\d+[A-Z0-9-]*', b[4])
                if match:
                    code = match.group(0).strip()
                    text_center_y = (b[1] + b[3]) / 2
                    
                    y_above = 0
                    y_below = page.rect.height
                    
                    for y in h_lines:
                        if y < text_center_y and y > y_above:
                            y_above = y
                        if y > text_center_y and y < y_below:
                            y_below = y
                            
                    if text_center_y - y_above > 100: y_above = text_center_y - 40
                    if y_below - text_center_y > 100: y_below = text_center_y + 40
                    
                    box_rect = fitz.Rect(40, y_above + 1, 125, y_below - 1)
                    pix = page.get_pixmap(clip=box_rect, dpi=300)
                    
                    filename = code + "_v6.png"
                    out_path = os.path.join(output_dir, filename)
                    pix.save(out_path)
                    extracted.append((code, filename))
                    
    return extracted

print("Extracting from PDF...")
extracted = extract_by_drawing(r"uploads/Kohler_PriceBook (June'26).pdf")
print(f"Extracted {len(extracted)} exact box images to _v6.png")

# Update search index
index_file = "search_index_v2.json"
with open(index_file, "r", encoding="utf-8") as f:
    db = json.load(f)

for code, filename in extracted:
    for item in db["stored_items"]:
        if code in item.get("search_code", ""):
            item["images"] = ["/static/images/Kohler/" + filename]

with open(index_file, "w", encoding="utf-8") as f:
    json.dump(db, f)

print("Updated search_index_v2.json with _v6.png paths!")

try:
    mongodb.save_search_index(db)
    print("Updated MongoDB search index!")
except Exception as e:
    print("Failed to update MongoDB:", e)
