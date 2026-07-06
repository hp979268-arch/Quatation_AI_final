import os, json

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
IMG_DIR    = r'C:\Movies\quotation-ai\quotation-ai\backend\static\images\Kohler'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
products = data['stored_items']
img_files = set(os.listdir(IMG_DIR))

reported = [
    'K-38519IN-0', 'K-26995IN-2-0', 'K-28786IN-0', 'K-27792IN-0',
    'K-28362IN-2-0', 'K-26994IN-HB1', 'K-26994IN-2-HB1',
    'K-17663IN-0', 'K-1286731',
    'K-38894IN-4ND-BV', 'K-38629IN-BV', 'K-26856IN-BV',
    'K-26855IN-BV', 'K-26349W-9-BV',
    'K-26855IN-AF', 'K-97168IN-AF', 'K-97167IN-AF', 'K-9301IN-CL-AF',
    'K-25348IN-BRD', '32989IN-NA', 'K-38629IN', 'K-30520IN-0',
    'K-25348IN-AF', 'K-73050T-B7-BV',
    'K-97360T-B4-CP', 'K-5584IN-0',
]

exts = ['.png', '.jpg', '.jpeg', '.webp']

def find_on_disk(code):
    for ext in exts:
        if code + ext in img_files:
            return code + ext
    code_lower = code.lower()
    for f in img_files:
        if f.lower().startswith(code_lower):
            return f
    return None

def find_in_index(code):
    code_clean = code.upper().strip()
    matches = []
    for p in products:
        if str(p.get('brand','')).lower() != 'kohler':
            continue
        name = str(p.get('name','')).upper()
        sc = str(p.get('search_code','')).upper()
        vc = str(p.get('variant_code','')).upper()
        if code_clean in name or code_clean in sc:
            matches.append(p)
    return matches

print(f"{'CODE':<25} {'DISK':^8} {'INDEX':^8} {'IMG_IN_INDEX':^12} {'IMG_ON_DISK':^12} NOTES")
print("-" * 100)

for code in reported:
    disk_file = find_on_disk(code)
    disk_status = "YES" if disk_file else "NO"

    index_entries = find_in_index(code)
    index_status = f"{len(index_entries)} entry" if index_entries else "NO"

    img_url_ok = "-"
    img_disk_ok = "-"
    notes = []

    if index_entries:
        for entry in index_entries[:1]:
            images = entry.get('images', [])
            if images:
                img_url = images[0]
                fname = img_url.split('/')[-1].split('?')[0]
                img_url_ok = "YES" if fname else "EMPTY"
                img_disk_ok = "YES" if fname in img_files else "NO"
                if img_disk_ok == "NO":
                    notes.append(f"URL points to '{fname}' (not on disk)")
            else:
                img_url_ok = "NO URL"
                img_disk_ok = "N/A"
                notes.append("No image URL in index")
    else:
        notes.append("Not in index at all")

    note_str = " | ".join(notes) if notes else ""
    print(f"{code:<25} {disk_status:^8} {index_status:^8} {img_url_ok:^12} {img_disk_ok:^12} {note_str}")
