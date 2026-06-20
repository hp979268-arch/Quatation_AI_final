import fitz

def get_images(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    return page.get_images()

print("March 112:", get_images(r"uploads/Kohler_Pricebook (March'26).pdf", 112))
print("June 114:", get_images(r"uploads/Kohler_PriceBook (June'26).pdf", 114))
