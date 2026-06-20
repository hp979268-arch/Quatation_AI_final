import fitz

def count_images(pdf_path):
    doc = fitz.open(pdf_path)
    total_images = 0
    all_xrefs = set()
    for page in doc:
        for img in page.get_images():
            all_xrefs.add(img[0])
            total_images += 1
    return total_images, len(all_xrefs)

march_tot, march_uniq = count_images(r"uploads/Kohler_Pricebook (March'26).pdf")
june_tot, june_uniq = count_images(r"uploads/Kohler_PriceBook (June'26).pdf")

print(f"March: {march_tot} total, {march_uniq} unique")
print(f"June:  {june_tot} total, {june_uniq} unique")
