import os
from PIL import Image
import numpy as np

def process_images():
    img_dir = "backend/static/images/Kohler"
    count_cropped = 0
    count_bg = 0
    
    for filename in os.listdir(img_dir):
        if filename.endswith(".png") and "K-" in filename and "_v" not in filename:
            filepath = os.path.join(img_dir, filename)
            try:
                img = Image.open(filepath).convert("RGBA")
                changed = False
                
                # 1. Check for wide aspect ratio (dual items)
                w, h = img.size
                if w > h * 1.5:
                    img = img.crop((0, 0, int(w*0.55), h))
                    changed = True
                    count_cropped += 1
                    
                # 2. Check for black background
                data = np.array(img)
                h2, w2 = data.shape[:2]
                
                if h2 >= 10 and w2 >= 10:
                    tl = data[0:5, 0:5]
                    br = data[h2-5:h2, w2-5:w2]
                    
                    if np.mean(tl[:, :, :3]) < 10 and np.mean(br[:, :, :3]) < 10:
                        r, g, b, a = data.T
                        black_areas = (r < 10) & (g < 10) & (b < 10)
                        data[..., 3][black_areas.T] = 0
                        
                        img2 = Image.fromarray(data)
                        bg = Image.new("RGBA", img2.size, (255, 255, 255, 255))
                        bg.paste(img2, mask=img2)
                        img = bg.convert("RGBA")
                        changed = True
                        count_bg += 1
                        
                if changed:
                    # Save as white background RGB to minimize size and alpha issues
                    final = Image.new("RGB", img.size, (255, 255, 255))
                    final.paste(img, mask=img.split()[3]) # paste using alpha as mask
                    final.save(filepath)
                    
            except Exception as e:
                print(f"Error on {filename}: {e}")
                
    print(f"Cropped {count_cropped} wide images.")
    print(f"Fixed {count_bg} black backgrounds.")

if __name__ == '__main__':
    process_images()
