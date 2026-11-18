import os
import sys
import zlib
import urllib.request
import time

def plantuml_encode(text: str) -> str:
    tbl = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    def encode64(data):
        r = ''
        for i in range(0, len(data), 3):
            b1 = data[i]
            b2 = data[i+1] if i+1 < len(data) else 0
            b3 = data[i+2] if i+2 < len(data) else 0
            c1 = b1 >> 2
            c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
            c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
            c4 = b3 & 0x3F
            r += tbl[c1] + tbl[c2]
            if i + 1 < len(data): r += tbl[c3]
            if i + 2 < len(data): r += tbl[c4]
        return r
    zlibbed = zlib.compress(text.encode('utf-8'))[2:-4]
    return encode64(zlibbed)

def render_file(puml_path: str, png_path: str):
    with open(puml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    code = plantuml_encode(content)
    url = f"http://www.plantuml.com/plantuml/png/{code}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                img_data = response.read()
                with open(png_path, 'wb') as out_f:
                    out_f.write(img_data)
                print(f"[OK] Rendered {os.path.basename(puml_path)} -> {os.path.basename(png_path)} ({len(img_data)} bytes)")
                return True
        except Exception as e:
            print(f"[Retry {attempt+1}] Error rendering {puml_path}: {e}")
            time.sleep(2)
    print(f"[FAILED] Could not render {puml_path}")
    return False

if __name__ == '__main__':
    uml_dir = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\uml"
    for f in sorted(os.listdir(uml_dir)):
        if f.endswith('.puml'):
            puml_file = os.path.join(uml_dir, f)
            png_file = os.path.join(uml_dir, f[:-5] + '.png')
            render_file(puml_file, png_file)
