import fitz
import os
from PIL import Image

doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
page = doc[124] # Page 125

# RGD: y=277. Closest images are Image 3 and Image 4.
# Wait, let's just get the full bounding box of the whole row for RGD
rect_rgd = fitz.Rect(40, 255, 110, 315)
pix_rgd = page.get_pixmap(clip=rect_rgd, dpi=300)
pix_rgd.save(r"static\images\Kohler\K-22786IN-4-RGD_v2.png")

# BV: y=344. Image 5 is at 339.
rect_bv = fitz.Rect(50, 310, 105, 365)
pix_bv = page.get_pixmap(clip=rect_bv, dpi=300)
pix_bv.save(r"static\images\Kohler\K-22786IN-4-BV_v2.png")

# BRD: y=531. Image 8 is at 532.
rect_brd = fitz.Rect(50, 510, 105, 555)
pix_brd = page.get_pixmap(clip=rect_brd, dpi=300)
pix_brd.save(r"static\images\Kohler\K-22786IN-4-BRD_v2.png")

# Also K-22789IN-4-RGD is on page 145. Let's find it.
doc_145 = doc[144]
rect_22789 = fitz.Rect(40, 255, 110, 315) # Guessing similar layout
pix_22789 = doc_145.get_pixmap(clip=rect_22789, dpi=300)
pix_22789.save(r"static\images\Kohler\K-22789IN-4-RGD_v2.png")

print("Saved all 4 images")
