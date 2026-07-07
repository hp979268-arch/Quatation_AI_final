import os, fitz
from PIL import Image

sc = 'K- 73050T-B7-AF'
JUNE_PDF = r"uploads/Kohler_PriceBook (June'26).pdf"

doc = fitz.open(JUNE_PDF)
page = doc[96]

# Find y of the text
blocks = page.get_text("dict")["blocks"]
found_y = None

for b in blocks:
    if "lines" not in b: continue
    for l in b["lines"]:
        for s in l["spans"]:
            text = s["text"].strip()
            if "73050" in text:
                found_y = s["bbox"][1]
                break
        if found_y: break
    if found_y: break

# Collect all image rects on the page
img_rects = []
for img_info in page.get_images(full=True):
    xref = img_info[0]
    for r in page.get_image_rects(xref):
        img_rects.append(r)

# Select the closest image rect vertically to our text
primary_rect = min(img_rects, key=lambda r: min(abs(r.y0 - found_y), abs(r.y1 - found_y)))
print(f"Primary selected image rect: {primary_rect}")

# Just crop the primary rect with a tiny padding (5 px)
final_rect = primary_rect + (-5, -5, 5, 5)
print(f"Final crop rect: {final_rect}")

pix = page.get_pixmap(clip=final_rect, matrix=fitz.Matrix(3, 3))
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

canvas_w = max(270, img.width + 40)
canvas_h = max(270, img.height + 40)

canvas = Image.new('RGB', (canvas_w, canvas_h), (255, 255, 255))
offset_x = (canvas_w - img.width) // 2
offset_y = (canvas_h - img.height) // 2
canvas.paste(img, (offset_x, offset_y))

output_path = "static/images/Kohler/K-73050T-B7-AF.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
canvas.save(output_path)
print(f"Saved cropped image to: {output_path}")
