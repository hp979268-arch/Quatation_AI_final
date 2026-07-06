import os
img_dir = r'c:\Movies\quotation-ai\quotation-ai\backend\static\images\Aquant'
needed = ['30006.png','30007.png','1320.png','1437.png','1419.png','1186.png','1418.png','2741.png']
for f in needed:
    exists = os.path.exists(os.path.join(img_dir, f))
    status = "EXISTS" if exists else "MISSING - needs manual upload"
    print(f + ": " + status)
