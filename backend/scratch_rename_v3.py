import json
import os
import shutil

index_file = "search_index_v2.json"
with open(index_file, "r", encoding="utf-8") as f:
    db = json.load(f)

for item in db["stored_items"]:
    if "images" in item and item["images"]:
        new_images = []
        for img in item["images"]:
            if "K-" in img and img.endswith("_v2.png"):
                # We need to check if this is one of the 40 items we updated.
                # Actually, we can just rename all _v2.png to _v3.png if we want to bust cache.
                new_img = img.replace("_v2.png", "_v3.png")
                
                # Rename the file on disk if it exists
                old_path = "." + img
                new_path = "." + new_img
                if os.path.exists(old_path):
                    shutil.move(old_path, new_path)
                
                new_images.append(new_img)
            else:
                new_images.append(img)
        item["images"] = new_images

with open(index_file, "w", encoding="utf-8") as f:
    json.dump(db, f)

print("Updated index and renamed to _v3.png")
