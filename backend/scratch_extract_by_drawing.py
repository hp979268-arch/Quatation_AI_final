import fitz
import os
import re

def extract_by_drawing(pdf_path):
    doc = fitz.open(pdf_path)
    output_dir = r"static\images\Kohler"
    
    extracted = []
    
    for page_num, page in enumerate(doc):
        blocks = page.get_text('blocks')
        drawings = page.get_drawings()
        
        # Find horizontal lines (where y0 == y1 and length is large)
        h_lines = []
        for d in drawings:
            for item in d["items"]:
                if item[0] == "l": # line
                    p1, p2 = item[1], item[2]
                    if abs(p1.y - p2.y) < 1: # horizontal
                        h_lines.append(p1.y)
                        
        h_lines.sort()
        
        for b in blocks:
            text = b[4].lower()
            if "trim + valve" in text or "trim & valve" in text:
                match = re.search(r'K-\d+[A-Z0-9-]*', b[4])
                if match:
                    code = match.group(0).strip()
                    text_center_y = (b[1] + b[3]) / 2
                    
                    # Find the closest horizontal line above and below
                    y_above = 0
                    y_below = page.rect.height
                    
                    for y in h_lines:
                        if y < text_center_y and y > y_above:
                            y_above = y
                        if y > text_center_y and y < y_below:
                            y_below = y
                            
                    # If we couldn't find lines, just use a fixed offset
                    if text_center_y - y_above > 100: y_above = text_center_y - 40
                    if y_below - text_center_y > 100: y_below = text_center_y + 40
                    
                    # The box is usually X=40 to X=120
                    # Let's add a small margin inside the lines
                    box_rect = fitz.Rect(40, y_above + 1, 125, y_below - 1)
                    
                    pix = page.get_pixmap(clip=box_rect, dpi=300)
                    
                    filename = code + "_v2.png"
                    out_path = os.path.join(output_dir, filename)
                    
                    pix.save(out_path)
                    extracted.append(code)
                    print(f"Extracted {code} using vector lines: {box_rect}")
                    
    return extracted

extracted = extract_by_drawing(r"uploads/Kohler_PriceBook (June'26).pdf")
print(f"Extracted {len(extracted)} exact box images.")
