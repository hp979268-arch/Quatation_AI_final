import fitz
doc = fitz.open(r"uploads/Kohler_PriceBook (June'26).pdf")
page = doc[114]
blocks = page.get_text('blocks')
for b in blocks:
    if "K-" in b[4] or "trim" in b[4]:
        print(f"Y0={b[1]:.1f}, Y1={b[3]:.1f}, Text={repr(b[4][:30])}")
