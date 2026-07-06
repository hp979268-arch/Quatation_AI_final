import os
import re

with open('c:/Movies/quotation-ai/quotation-ai/backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '/upload-image' not in content:
    new_route = '''
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1]
        if not ext:
            ext = ".png"
        safe_name = f"manual_{int(datetime.now().timestamp())}_{_sanitize_filename(file.filename, 'image' + ext)}"
        upload_dir = os.path.join(STATIC_DIR, "images", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, safe_name)
        content = await file.read()
        with open(path, "wb") as buffer:
            buffer.write(content)
        return {"url": f"/static/images/uploads/{safe_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
    parts = content.split('async def upload_pdf(')
    assert len(parts) == 2
    
    rest = parts[1]
    end_of_func = rest.find('@app.post')
        
    assert end_of_func != -1
    
    final_content = parts[0] + 'async def upload_pdf(' + rest[:end_of_func] + new_route + '\n' + rest[end_of_func:]
    
    with open('c:/Movies/quotation-ai/quotation-ai/backend/main.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print('Added /upload-image route')
else:
    print('Route already exists')
