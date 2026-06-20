from PIL import Image
import os

img_dir = "backend/static/images/Kohler"
wide_images = []

for filename in os.listdir(img_dir):
    if filename.endswith(".png") and "K-" in filename and "_v" not in filename:
        filepath = os.path.join(img_dir, filename)
        try:
            with Image.open(filepath) as img:
                w, h = img.size
                if w > h * 1.5:  # Wide aspect ratio, likely dual items
                    wide_images.append(filename)
        except:
            pass

print(f"Found {len(wide_images)} wide images.")
if wide_images:
    print("Examples:", wide_images[:10])
    
    # Let's crop one as a test
    test_img = os.path.join(img_dir, wide_images[0])
    img = Image.open(test_img)
    w, h = img.size
    # Crop left half
    left_half = img.crop((0, 0, int(w*0.55), h))
    left_half.save("artifacts/test_half_crop.png")
    print("Saved test crop to artifacts/test_half_crop.png")
