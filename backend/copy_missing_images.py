import shutil, os, json

IMG_DIR = r"c:\Movies\quotation-ai\quotation-ai\backend\static\images\Aquant"
INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"

# Copy existing CP images to generic names for non-CP variants
copies = [
    ("1419CP.png",  "1419.png"),
    ("1186CP.png",  "1186.png"),
    ("1418CP.png",  "1418.png"),
    ("2741CP.png",  "2741.png"),
    ("1424CP.png",  "1424.png"),
]

for src, dst in copies:
    src_path = os.path.join(IMG_DIR, src)
    dst_path = os.path.join(IMG_DIR, dst)
    if os.path.exists(src_path) and not os.path.exists(dst_path):
        shutil.copy2(src_path, dst_path)
        print(f"  [COPY] {src} -> {dst}")
    elif os.path.exists(dst_path):
        print(f"  [OK]   {dst} already exists")
    else:
        print(f"  [ERR]  {src} not found!")

print("\nDone. All images ready.")
