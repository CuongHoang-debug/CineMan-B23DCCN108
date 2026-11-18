import threading
import time
import os
import subprocess
import sys

sys.path.append(r'C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\src')
from app import app

SCREENSHOT_DIR = r'C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\screenshots'
EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

def run_server():
    app.run(port=5007, use_reloader=False)

def capture_page(url, output_png, wait_sec=2):
    args = [
        EDGE_PATH,
        '--headless',
        '--disable-gpu',
        '--window-size=1280,850',
        f'--screenshot={output_png}',
        url
    ]
    subprocess.run(args, check=True)
    print(f"[OK] Captured: {os.path.basename(output_png)} ({os.path.getsize(output_png)} bytes)")

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(2)

    # 6. Movie Management
    capture_page('http://127.0.0.1:5007/dev-login/QUAN_LY/movies', os.path.join(SCREENSHOT_DIR, '06_giao_dien_quan_ly_phim.png'))

    # 7. Schedule Management
    capture_page('http://127.0.0.1:5007/dev-login/QUAN_LY/schedules', os.path.join(SCREENSHOT_DIR, '07_giao_dien_quan_ly_lich_chieu.png'))

    print("All screenshots successfully captured!")
    sys.exit(0)
