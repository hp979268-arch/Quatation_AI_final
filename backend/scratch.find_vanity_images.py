import os

image_dir = "backend/static/images"

search_patterns = [
    "vanity", "oak", "grey", "soundtile", "speaker", "amplifier", "anthem", "enclosure", "sliding", "hardware", "extn", "extension"
]

all_files = []
for root, _, files in os.walk(image_dir):
    for f in files:
        all_files.append(os.path.join(root, f).replace("\\", "/"))

matches = {}
for p in search_patterns:
    matches[p] = []
    for f in all_files:
        if p in f.lower():
            matches[p].append(f)

for p, paths in matches.items():
    print(f"Pattern '{p}': {len(paths)} matches")
    for x in paths[:5]:
        print(f"  - {x}")
