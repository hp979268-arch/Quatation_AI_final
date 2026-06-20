import json

def main():
    print("Loading database for deduplication...")
    with open('search_index_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('stored_items', [])
    print(f"Original items: {len(items)}")
    
    seen = {}
    deduped = []
    
    # Iterate backwards so we keep the LAST occurrence (the recently injected fixed ones)
    for i in range(len(items)-1, -1, -1):
        item = items[i]
        code = item.get('search_code')
        if not code:
            deduped.append(item)
            continue
            
        if code in seen:
            continue
            
        seen[code] = True
        deduped.append(item)
        
    # Reverse back to original order
    deduped.reverse()
    
    print(f"Items after deduplication: {len(deduped)}")
    print(f"Removed {len(items) - len(deduped)} duplicates.")
    
    data['stored_items'] = deduped
    
    # Now run the maintenance scripts to rebuild keyword index
    import maintenance
    maintenance.clean_junk_entries(data)
    maintenance.rebuild_keyword_index(data)
    maintenance.crop_multi_part_images(data) # Just in case, though they are already cropped
    
    with open('search_index_v2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    maintenance.sync_to_mongodb(data)
    
    import shutil
    import os
    local_app_data = os.path.expandvars(r"%LOCALAPPDATA%\Shreeji Ceramica\search_index_v2.json")
    if os.path.exists(os.path.dirname(local_app_data)):
        shutil.copy2('search_index_v2.json', local_app_data)
        
    print("Deduplication complete!")

if __name__ == '__main__':
    main()
