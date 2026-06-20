import fitz

doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
for p in doc:
    text = p.get_text()
    if '29199' in text:
        print(f"Page {p.number}")
        for b in p.get_text('blocks'):
            if '29199' in b[4]:
                print(f"BBOX: {b[:4]} - {b[4].strip()}")
        print("Images on this page:")
        for img in p.get_images(full=True):
            for r in p.get_image_rects(img[0]):
                print(f"Image {img[0]}: {r}")
