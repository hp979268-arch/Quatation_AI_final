import json
import time
import subprocess

INDEX_PATH = "search_index_v2.json"

print(f"Loading {INDEX_PATH}...")
with open(INDEX_PATH, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# Bump version timestamp
old_version = data.get("version", "unknown")
new_version = str(int(time.time()))
data["version"] = new_version
print(f"Bumping version: {old_version} -> {new_version}")

# Save index
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved updated index locally.")

# Execute mongo push script
print("Running direct_mongo_push.py...")
res = subprocess.run([r"..\.venv\Scripts\python.exe", "direct_mongo_push.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
