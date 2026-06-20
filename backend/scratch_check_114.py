import fitz

doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
page = doc[114]
blocks = page.get_text('blocks')
for b in blocks:
    if "22786" in b[4]:
        print("Text:", b)

print("\nImages:")
for img in page.get_images():
    rects = page.get_image_rects(img[0])
    for r in rects:
        print(f"Image {img[0]}: {r}")
