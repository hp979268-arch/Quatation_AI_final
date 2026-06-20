import os
from PIL import Image
import numpy as np

def fix_all_black_backgrounds():
    img_dir = "backend/static/images/Kohler"
    if not os.path.exists(img_dir):
        print("Directory not found!")
        return

    count = 0
    for filename in os.listdir(img_dir):
        if filename.endswith(".png") and "K-" in filename and "_v" not in filename:
            filepath = os.path.join(img_dir, filename)
            try:
                img = Image.open(filepath).convert("RGBA")
                data = np.array(img)
                
                # Check corners to see if they are black
                # A robust check: if the top-left and bottom-right corners are both black
                h, w = data.shape[:2]
                if h < 10 or w < 10:
                    continue
                    
                tl = data[0:5, 0:5]
                br = data[h-5:h, w-5:w]
                
                def is_black(region):
                    return np.mean(region[:, :, :3]) < 10
                    
                if is_black(tl) and is_black(br):
                    # It has a black background! Fix it!
                    r, g, b, a = data.T
                    black_areas = (r < 10) & (g < 10) & (b < 10)
                    data[..., 3][black_areas.T] = 0
                    
                    img2 = Image.fromarray(data)
                    bg = Image.new("RGBA", img2.size, (255, 255, 255, 255))
                    bg.paste(img2, mask=img2)
                    bg.convert("RGB").save(filepath) # Overwrite original
                    
                    count += 1
                    print(f"Fixed black background for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    print(f"Fixed a total of {count} images.")

if __name__ == '__main__':
    fix_all_black_backgrounds()
