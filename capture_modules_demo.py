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
    app.run(port=5010, use_reloader=False)

def capture_page(url, output_png, delay=1.5):
    # Give browser a short sleep if needed by opening via edge
    args = [
        EDGE_PATH,
        '--headless',
        '--disable-gpu',
        '--window-size=1280,850',
        f'--screenshot={output_png}',
        url
    ]
    time.sleep(delay)
    subprocess.run(args, check=True)
    print(f"[OK] Captured: {os.path.basename(output_png)} ({os.path.getsize(output_png)} bytes)")

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(2)

    # ================= MODULE 1: ĐĂNG KÝ THÀNH VIÊN =================
    print("[*] Chụp Module 1: Khách hàng đăng ký thành viên...")
    # Bước 1 & 2: Form đăng ký nhập thông tin
    capture_page('http://127.0.0.1:5010/demo/register-filled', os.path.join(SCREENSHOT_DIR, 'mod1_01_form_dangky.png'))
    # Bước 3: Thông báo thành công & cấp mã thẻ
    capture_page('http://127.0.0.1:5010/demo/register-success', os.path.join(SCREENSHOT_DIR, 'mod1_02_thongbao_thanhcong.png'))
    # Bước 4: Dữ liệu lưu trong CSDL SQLite
    capture_page('http://127.0.0.1:5010/demo/sqlite-view', os.path.join(SCREENSHOT_DIR, 'mod1_03_csdl_sqlite.png'))

    # ================= MODULE 2: NHÂN VIÊN BÁN VÉ TẠI QUẦY (POS) =================
    print("[*] Chụp Module 2: Nhân viên bán vé tại quầy...")
    # Bước 1: Chọn menu bán vé (màn hình POS ban đầu)
    capture_page('http://127.0.0.1:5010/dev-login/BAN_HANG', os.path.join(SCREENSHOT_DIR, 'mod2_01_menu_banve.png'), delay=1.0)
    # Bước 2: Hỏi tên phim & tìm phim (gõ tìm 'Dune')
    capture_page('http://127.0.0.1:5010/dev-login/BAN_HANG?demo_step=search', os.path.join(SCREENSHOT_DIR, 'mod2_02_tim_va_chon_phim.png'), delay=1.2)
    # Bước 3: Chọn phim từ danh sách kết quả -> hiển thị giờ xem
    capture_page('http://127.0.0.1:5010/dev-login/BAN_HANG?demo_step=select_movie', os.path.join(SCREENSHOT_DIR, 'mod2_03_chon_gio_xem.png'), delay=1.2)
    # Bước 4: Chọn giờ xem -> hiển thị sơ đồ ghế -> chọn ghế VIP D04, D05
    capture_page('http://127.0.0.1:5010/dev-login/BAN_HANG?demo_step=select_seats', os.path.join(SCREENSHOT_DIR, 'mod2_04_chon_ghe.png'), delay=2.0)
    # Bước 5: Nhập mã thẻ thân thiết MB-8888 -> chiết khấu VIP 15% & xác nhận mua vé
    capture_page('http://127.0.0.1:5010/dev-login/BAN_HANG?demo_step=apply_card', os.path.join(SCREENSHOT_DIR, 'mod2_05_nhap_the_thanh_vien.png'), delay=2.5)
    # Bước 6 & 7: Thanh toán & In vé, hóa đơn
    capture_page('http://127.0.0.1:5010/invoice/1', os.path.join(SCREENSHOT_DIR, 'mod2_06_in_ve_hoa_don.png'), delay=1.0)

    print("[DONE] Hoàn tất chụp ảnh 2 Module!")
    sys.exit(0)
