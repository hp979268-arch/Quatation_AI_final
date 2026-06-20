import os
from PIL import Image
import numpy as np

def fix_special_finishes():
    img_dir = "backend/static/images/Kohler"
    target_suffixes = ["-AF.png", "-BV.png", "-RGD.png", "-BRD.png", "-BN.png", " AF.png", " BV.png", " RGD.png", " BRD.png", " BN.png"]
    count = 0
    
    for filename in os.listdir(img_dir):
        if any(filename.endswith(sfx) for sfx in target_suffixes) and "_v" not in filename:
            filepath = os.path.join(img_dir, filename)
            try:
                img = Image.open(filepath).convert("RGBA")
                w, h = img.size
                
                # 1. Crop left 55%
                img = img.crop((0, 0, int(w * 0.55), h))
                
                # 2. Remove black background
                data = np.array(img)
                r, g, b, a = data.T
                
                # We consider pixels black if R<30, G<30, B<30
                black_areas = (r < 30) & (g < 30) & (b < 30)
                data[..., 3][black_areas.T] = 0
                
                img2 = Image.fromarray(data)
                bg = Image.new("RGBA", img2.size, (255, 255, 255, 255))
                bg.paste(img2, mask=img2)
                
                # Save as RGB to eliminate alpha channel completely
                bg.convert("RGB").save(filepath)
                count += 1
                
            except Exception as e:
                print(f"Error on {filename}: {e}")
                
    print(f"Processed {count} special finish images.")

if __name__ == '__main__':
    fix_special_finishes()
