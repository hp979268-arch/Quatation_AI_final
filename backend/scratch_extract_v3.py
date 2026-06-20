import fitz
import re
import os

def extract_combined_images_v3(pdf_path):
    doc = fitz.open(pdf_path)
    output_dir = r"static\images\Kohler"
    
    extracted = []
    
    for page_num, page in enumerate(doc):
        blocks = page.get_text('blocks')
        images = page.get_images()
        
        # Get bounding boxes for all images on page
        img_rects = []
        for img in images:
            xref = img[0]
            try:
                rects = page.get_image_rects(xref)
                if rects:
                    img_rects.append(rects[0])
            except:
                pass
                
        for b in blocks:
            text = b[4].lower()
            if "trim + valve" in text or "trim & valve" in text:
                match = re.search(r'K-\d+[A-Z0-9-]*', b[4])
                if match:
                    code = match.group(0).strip()
                    text_y0, text_y1 = b[1], b[3]
                    text_center_y = (text_y0 + text_y1) / 2
                    
                    row_images = []
                    for r in img_rects:
                        img_center_y = (r.y0 + r.y1) / 2
                        if abs(img_center_y - text_center_y) < 30: # strict threshold!
                            row_images.append(r)
                            
                    if row_images:
                        # Combine all image rects
                        combined_rect = row_images[0]
                        for r in row_images[1:]:
                            combined_rect = combined_rect | r
                            
                        # Add a small padding (5 points)
                        combined_rect = combined_rect + (-5, -5, 5, 5)
                        
                        pix = page.get_pixmap(clip=combined_rect, dpi=300)
                        
                        filename = code + "_v2.png"
                        out_path = os.path.join(output_dir, filename)
                        
                        pix.save(out_path)
                        extracted.append(code)
                        print(f"Extracted {code} with {len(row_images)} images, Y={text_center_y:.1f}")
    
    return extracted

extracted = extract_combined_images_v3(r"uploads/Kohler_PriceBook (June'26).pdf")
print(f"Extracted {len(extracted)} clean images.")
