import fitz

doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
page = doc[124] # Page 125

print("Searching for 22786 on Page 125:")
for b in page.get_text('blocks'):
    text = b[4].strip()
    if '22786' in text or '22789' in text or '72328' in text or '72290' in text:
        print(f"BBOX: {b[:4]}")
        print(f"TEXT: {text}\n")
        
print("Images on Page 125:")
for img in page.get_images(full=True):
    rects = page.get_image_rects(img[0])
    for r in rects:
        print(f"Image {img[0]}: {r}")
