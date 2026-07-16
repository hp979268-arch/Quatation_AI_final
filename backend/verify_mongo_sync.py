import json
import sys
import os
from dotenv import load_dotenv

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
load_dotenv(os.path.join(backend_dir, '.env'), override=True)
import mongodb

with open(os.path.join(backend_dir, 'search_index_v2.json'), 'r', encoding='utf-8') as f:
    local_data = json.load(f)

print('Local Index Version:', local_data.get('version'))
print('Total Items Local:', len(local_data.get('stored_items', [])))

print('\nFetching from MongoDB...')
remote_data = mongodb.load_search_index()
if not remote_data:
    print('Failed to load from MongoDB!')
else:
    print('MongoDB Index Version:', remote_data.get('version'))
    print('Total Items MongoDB:', len(remote_data.get('stored_items', [])))
    
    local_item = next((p for p in local_data['stored_items'] if p.get('search_code') == 'K-38896IN-4FS-BV'), None)
    remote_item = next((p for p in remote_data['stored_items'] if p.get('search_code') == 'K-38896IN-4FS-BV'), None)
    
    print('\nVerifying specific fixes in MongoDB:')
    print(f"K-38896IN-4FS-BV -> Local Price: {local_item.get('price')} | Remote Price: {remote_item.get('price')}")
    
    aquant_5141_mb_local = next((p for p in local_data['stored_items'] if p.get('search_code') == '5141 MB'), None)
    aquant_5141_mb_remote = next((p for p in remote_data['stored_items'] if p.get('search_code') == '5141 MB'), None)
    if aquant_5141_mb_local and aquant_5141_mb_remote:
        print(f"Aquant 5141 MB -> Local Price: {aquant_5141_mb_local.get('price')} | Remote Price: {aquant_5141_mb_remote.get('price')}")
