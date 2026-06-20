from PIL import Image
import numpy as np

def fix_black_background(img_path):
    img = Image.open(img_path).convert("RGBA")
    data = np.array(img)
    
    r, g, b, a = data.T
    
    # Define black threshold
    black_areas = (r < 10) & (g < 10) & (b < 10)
    
    # Change black areas to transparent
    data[..., 3][black_areas.T] = 0
    
    img2 = Image.fromarray(data)
    img2.save(img_path.replace(".png", "_nobg.png"))
    
    # Also create a white background version
    bg = Image.new("RGBA", img2.size, (255, 255, 255, 255))
    bg.paste(img2, mask=img2)
    bg.convert("RGB").save(img_path.replace(".png", "_white.png"))

fix_black_background("artifacts/compare2/K-27483IN-4ND-AF.png")
print("Done")
