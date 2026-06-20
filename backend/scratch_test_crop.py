import fitz
from PIL import Image
import os

doc = fitz.open(r"backend/uploads/Kohler_PriceBook (June'26).pdf")
p = doc[53]

# Let's extract the image for K-27482IN-4ND-CP
# Its text is around Y:70.4-89.9
y_above = 70.4 - 20
y_below = 89.9 + 50

# Crop from X=30 to X=90
rect = fitz.Rect(30, y_above, 90, y_below)
pix = p.get_pixmap(clip=rect, dpi=300)
pix.save("artifacts/test_crop.png")

# Crop the full width (X=20 to X=150) to see what we are cutting off
rect_full = fitz.Rect(20, y_above, 150, y_below)
pix_full = p.get_pixmap(clip=rect_full, dpi=300)
pix_full.save("artifacts/test_full.png")

print("Saved test crops")
