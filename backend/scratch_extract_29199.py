import fitz

doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
page = doc[121] # Page 122

rect = fitz.Rect(45, 685, 115, 730)
pix = page.get_pixmap(clip=rect, dpi=300)
pix.save(r"static\images\Kohler\K-29199IN-ECH-RGD_v2.png")
print("Saved 29199 image")
