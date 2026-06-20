import fitz

doc = fitz.open(r"backend/uploads/Kohler_PriceBook (June'26).pdf")
for p in doc:
    for b in p.get_text('blocks'):
        if '21970' in b[4]:
            print(b[4])
