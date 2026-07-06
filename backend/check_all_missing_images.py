import json, os

INDEX_PATH = r"c:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json"
IMG_DIR = r"c:\Movies\quotation-ai\quotation-ai\backend\static\images\Aquant"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
items = data["stored_items"]

existing = set(os.listdir(IMG_DIR))

# All products we touched / added - check unique image files needed
touched_bases = [
    "30006","30007","1320-750","1437-750","1419","1186","1418","2741",
    "1424-200","1424-500","1424",
    # price fixed ones - check their images too
    "1501","1506","1507","1947","9057","1258","1257","1256","1245","1439",
    "28088","28197","28198","1151","1152","1153","1460","1462","1487","1461",
    "1010","1436","1318","1319","60080 BS","750080 BS","90080 BS",
    "7011","2650","2750","2728","2726","2729","2721","1472",
    "2106","2104","2122","2114","1025"
]

# Collect unique image filenames needed
missing_images = {}  # filename -> [products using it]
ok_images = {}

seen_files = set()
for item in items:
    bc = item.get("base_code","")
    if bc not in touched_bases:
        continue
    imgs = item.get("images", [])
    if not imgs:
        sc = item.get("search_code","?")
        key = "NO_IMAGE_URL"
        missing_images.setdefault(key, []).append(sc)
        continue
    for img_url in imgs:
        fname = img_url.split("/")[-1].split("?")[0]
        if fname in seen_files:
            continue
        seen_files.add(fname)
        if fname in existing:
            ok_images[fname] = bc
        else:
            missing_images.setdefault(fname, []).append(item.get("search_code","?"))

print("=" * 50)
print("IMAGES MISSING (aapko dene honge):")
print("=" * 50)
count = 0
for fname, products in missing_images.items():
    if fname == "NO_IMAGE_URL":
        print(f"\n  [NO URL] Products with no image URL set:")
        for p in products[:5]:
            print(f"    - {p}")
    else:
        count += 1
        print(f"  {count}. {fname}")
        print(f"     Used by: {', '.join(set(products[:3]))}")

print(f"\nTotal missing image files: {count}")
print("\n" + "=" * 50)
print("IMAGES ALREADY EXIST (kuch karne ki zarurat nahi):")
print("=" * 50)
for fname in sorted(ok_images.keys()):
    print(f"  [OK] {fname}")
