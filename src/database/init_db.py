import sqlite3
import os
import hashlib
from datetime import datetime, date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'cineman.db')

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Kich hoat Foreign Key
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Bang Nguoi Dung
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblNguoiDung (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        taiKhoan TEXT UNIQUE NOT NULL,
        matKhau TEXT NOT NULL,
        hoTen TEXT NOT NULL,
        sdt TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        vaiTro TEXT NOT NULL, -- 'QUAN_LY', 'BAN_HANG', 'KHACH_HANG'
        ngayTao DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # 2. Bang Nhan Vien
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblNhanVien (
        id INTEGER PRIMARY KEY,
        chucVu TEXT NOT NULL,
        caLamViec TEXT,
        luongCoBan REAL,
        FOREIGN KEY (id) REFERENCES tblNguoiDung(id) ON DELETE CASCADE
    );
    ''')

    # 3. Bang Khach Hang
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblKhachHang (
        id INTEGER PRIMARY KEY,
        cccd TEXT UNIQUE NOT NULL,
        ngaySinh DATE,
        diaChi TEXT,
        FOREIGN KEY (id) REFERENCES tblNguoiDung(id) ON DELETE CASCADE
    );
    ''')

    # 4. Bang The Thanh Vien
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblTheThanhVien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        maThe TEXT UNIQUE NOT NULL,
        idKhachHang INTEGER UNIQUE NOT NULL,
        hangThe TEXT DEFAULT 'Standard', -- 'Standard', 'Silver', 'Gold', 'VIP'
        diemTichLuy INTEGER DEFAULT 0,
        ngayCap DATE DEFAULT (date('now')),
        trangThai TEXT DEFAULT 'HOAT_DONG',
        FOREIGN KEY (idKhachHang) REFERENCES tblKhachHang(id) ON DELETE CASCADE
    );
    ''')

    # 5. Bang Phim
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblPhim (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenPhim TEXT NOT NULL,
        theLoai TEXT NOT NULL,
        thoiLuong INTEGER NOT NULL,
        daoDien TEXT,
        dienVien TEXT,
        doTuoi TEXT DEFAULT 'P',
        poster TEXT,
        moTa TEXT,
        trangThai TEXT DEFAULT 'DANG_CHIEU'
    );
    ''')

    # 6. Bang Phong Chieu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblPhongChieu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenPhong TEXT NOT NULL,
        loaiPhong TEXT DEFAULT '2D',
        tongSoGhe INTEGER NOT NULL
    );
    ''')

    # 7. Bang Ghe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblGhe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idPhong INTEGER NOT NULL,
        maGhe TEXT NOT NULL,
        soHang TEXT NOT NULL,
        soCot INTEGER NOT NULL,
        loaiGhe TEXT DEFAULT 'THUONG', -- 'THUONG', 'VIP', 'SWEETBOX'
        phuThu REAL DEFAULT 0,
        FOREIGN KEY (idPhong) REFERENCES tblPhongChieu(id) ON DELETE CASCADE
    );
    ''')

    # 8. Bang Lich Chieu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblLichChieu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idPhim INTEGER NOT NULL,
        idPhong INTEGER NOT NULL,
        ngayChieu DATE NOT NULL,
        gioBatDau TIME NOT NULL,
        gioKetThuc TIME NOT NULL,
        giaVeGoc REAL NOT NULL,
        FOREIGN KEY (idPhim) REFERENCES tblPhim(id) ON DELETE CASCADE,
        FOREIGN KEY (idPhong) REFERENCES tblPhongChieu(id) ON DELETE CASCADE
    );
    ''')

    # 9. Bang Hoa Don
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblHoaDon (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        maHD TEXT UNIQUE NOT NULL,
        idNhanVien INTEGER NOT NULL,
        idKhachHang INTEGER,
        ngayLap DATETIME DEFAULT CURRENT_TIMESTAMP,
        tongTien REAL NOT NULL,
        giamGia REAL DEFAULT 0,
        thanhTien REAL NOT NULL,
        phuongThucTT TEXT DEFAULT 'TIEN_MAT',
        FOREIGN KEY (idNhanVien) REFERENCES tblNhanVien(id),
        FOREIGN KEY (idKhachHang) REFERENCES tblKhachHang(id)
    );
    ''')

    # 10. Bang Ve
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tblVe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        maVe TEXT UNIQUE NOT NULL,
        idLichChieu INTEGER NOT NULL,
        idGhe INTEGER NOT NULL,
        idHoaDon INTEGER NOT NULL,
        giaBan REAL NOT NULL,
        ngayBan DATETIME DEFAULT CURRENT_TIMESTAMP,
        trangThai TEXT DEFAULT 'DA_BAN',
        FOREIGN KEY (idLichChieu) REFERENCES tblLichChieu(id),
        FOREIGN KEY (idGhe) REFERENCES tblGhe(id),
        FOREIGN KEY (idHoaDon) REFERENCES tblHoaDon(id) ON DELETE CASCADE
    );
    ''')

    # Xoa du lieu cu neu can reset
    cursor.execute("SELECT COUNT(*) FROM tblNguoiDung")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()
    print("[OK] Khoi tao CSDL CineMan thanh cong!")

def seed_data(cursor):
    print("[*] Chen du lieu mau...")

    # Chen Nguoi Dung
    users = [
        ('admin', hash_pw('admin123'), 'Trần Đức Quản Lý', '0912345678', 'admin@cineman.vn', 'QUAN_LY'),
        ('staff', hash_pw('staff123'), 'Nguyễn Thu Ngân', '0923456789', 'staff@cineman.vn', 'BAN_HANG'),
        ('customer', hash_pw('customer123'), 'Lê Văn Khách', '0934567890', 'customer@gmail.com', 'KHACH_HANG'),
        ('hoangnam', hash_pw('pass123'), 'Hoàng Thị Nam', '0945678901', 'namht@gmail.com', 'KHACH_HANG')
    ]
    cursor.executemany('''
    INSERT INTO tblNguoiDung (taiKhoan, matKhau, hoTen, sdt, email, vaiTro)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', users)

    # Nhan vien
    cursor.execute("INSERT INTO tblNhanVien (id, chucVu, caLamViec, luongCoBan) VALUES (1, 'Quản lý rạp', 'Hành chính', 15000000)")
    cursor.execute("INSERT INTO tblNhanVien (id, chucVu, caLamViec, luongCoBan) VALUES (2, 'Nhân viên bán vé', 'Ca sáng/chiều', 7000000)")

    # Khach hang
    cursor.execute("INSERT INTO tblKhachHang (id, cccd, ngaySinh, diaChi) VALUES (3, '001201009988', '1998-05-15', 'Hà Đông, Hà Nội')")
    cursor.execute("INSERT INTO tblKhachHang (id, cccd, ngaySinh, diaChi) VALUES (4, '001202008877', '2001-11-20', 'Cầu Giấy, Hà Nội')")

    # The thanh vien
    cursor.execute("INSERT INTO tblTheThanhVien (maThe, idKhachHang, hangThe, diemTichLuy) VALUES ('MB-8888', 3, 'VIP', 450)")
    cursor.execute("INSERT INTO tblTheThanhVien (maThe, idKhachHang, hangThe, diemTichLuy) VALUES ('MB-9999', 4, 'Gold', 210)")

    # Phim
    movies = [
        ('Đào, Phở và Piano', 'Lịch sử / Chiến tranh', 100, 'Phi Tiến Sơn', 'Doãn Quốc Đam, Cao Thùy Linh', 'P', 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500', 'Tác phẩm tái hiện không khí quả cảm của quân dân thủ đô trong 60 ngày đêm khói lửa năm 1946.', 'DANG_CHIEU'),
        ('Dune: Hành Tinh Cát - Phần 2', 'Khoa học viễn tưởng / Phiêu lưu', 166, 'Denis Villeneuve', 'Timothée Chalamet, Zendaya', 'T16', 'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500', 'Paul Atreides liên minh cùng Chani và người Fremen để trả thù những kẻ đã hủy diệt gia tộc anh.', 'DANG_CHIEU'),
        ('Mai', 'Tâm lý / Tình cảm / Gia đình', 131, 'Trấn Thành', 'Phương Anh Đào, Tuấn Trần', 'T18', 'https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=500', 'Câu chuyện về Mai - một phụ nữ làm nghề massage trị liệu và mối tình nhiều trắc trở với chàng nhạc công Sâu.', 'DANG_CHIEU'),
        ('Kung Fu Panda 4', 'Hoạt hình / Hài hước / Hành động', 94, 'Mike Mitchell', 'Jack Black, Awkwafina', 'P', 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500', 'Po bước vào hành trình tìm kiếm người kế vị Thần Long Đại Hiệp và đối đầu mụ Tắc Kè Bông xảo quyệt.', 'DANG_CHIEU'),
        ('Godzilla x Kong: Đế Chế Mới', 'Hành động / Viễn tưởng', 115, 'Adam Wingard', 'Rebecca Hall, Brian Tyree Henry', 'T13', 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=500', 'Hai quái thú huyền thoại hợp lực chống lại một mối đe dọa khổng lồ giấu mình trong Trái Đất rỗng.', 'DANG_CHIEU')
    ]
    cursor.executemany('''
    INSERT INTO tblPhim (tenPhim, theLoai, thoiLuong, daoDien, dienVien, doTuoi, poster, moTa, trangThai)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', movies)

    # Phong chieu
    rooms = [
        ('Cinema Hall 01 (IMAX)', 'IMAX', 48),
        ('Cinema Hall 02 (3D)', '3D', 40),
        ('Cinema Hall 03 (Standard)', '2D', 40)
    ]
    cursor.executemany('INSERT INTO tblPhongChieu (tenPhong, loaiPhong, tongSoGhe) VALUES (?, ?, ?)', rooms)

    # Tao ghe cho tung phong
    # Phong 1: 6 hang (A, B, C: Thuong; D, E: VIP; F: Sweetbox) x 8 cot
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    for r_idx, r in enumerate(rows):
        for c in range(1, 9):
            code = f"{r}{c:02d}"
            if r in ['A', 'B', 'C']:
                l_ghe = 'THUONG'
                phu_thu = 0.0
            elif r in ['D', 'E']:
                l_ghe = 'VIP'
                phu_thu = 20000.0
            else:
                l_ghe = 'SWEETBOX'
                phu_thu = 50000.0
            cursor.execute('''
            INSERT INTO tblGhe (idPhong, maGhe, soHang, soCot, loaiGhe, phuThu)
            VALUES (1, ?, ?, ?, ?, ?)
            ''', (code, r, c, l_ghe, phu_thu))

    # Phong 2 & 3: 5 hang x 8 cot
    for p_id in [2, 3]:
        for r in ['A', 'B', 'C', 'D', 'E']:
            for c in range(1, 9):
                code = f"{r}{c:02d}"
                l_ghe = 'VIP' if r in ['C', 'D'] else 'THUONG'
                phu_thu = 15000.0 if l_ghe == 'VIP' else 0.0
                cursor.execute('''
                INSERT INTO tblGhe (idPhong, maGhe, soHang, soCot, loaiGhe, phuThu)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (p_id, code, r, c, l_ghe, phu_thu))

    # Lich chieu hom nay & ngay mai
    today = date.today().strftime('%Y-%m-%d')
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    schedules = [
        # Phim 1: Dao Pho va Piano
        (1, 1, today, '09:30', '11:10', 85000.0),
        (1, 1, today, '14:00', '15:40', 95000.0),
        (1, 1, today, '19:30', '21:10', 105000.0),
        # Phim 2: Dune 2
        (2, 1, today, '16:00', '18:46', 110000.0),
        (2, 1, today, '21:30', '00:16', 110000.0),
        # Phim 3: Mai
        (3, 2, today, '10:00', '12:11', 85000.0),
        (3, 2, today, '15:00', '17:11', 95000.0),
        (3, 2, today, '20:00', '22:11', 105000.0),
        # Phim 4: Kung Fu Panda
        (4, 3, today, '09:00', '10:34', 80000.0),
        (4, 3, today, '13:30', '15:04', 85000.0),
        (4, 3, today, '17:00', '18:34', 90000.0),
        # Ngay mai
        (1, 1, tomorrow, '10:00', '11:40', 85000.0),
        (2, 1, tomorrow, '14:30', '17:16', 110000.0),
        (5, 2, tomorrow, '19:00', '20:55', 95000.0)
    ]
    cursor.executemany('''
    INSERT INTO tblLichChieu (idPhim, idPhong, ngayChieu, gioBatDau, gioKetThuc, giaVeGoc)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', schedules)

    # Chen mot so Hoa don & Ve mau de phuc vu thong ke
    cursor.execute('''
    INSERT INTO tblHoaDon (maHD, idNhanVien, idKhachHang, ngayLap, tongTien, giamGia, thanhTien, phuongThucTT)
    VALUES ('HD-20261101-001', 2, 3, '2026-11-01 10:15:00', 210000, 21000, 189000, 'TIEN_MAT')
    ''')
    hd1_id = cursor.lastrowid
    cursor.execute('''
    INSERT INTO tblVe (maVe, idLichChieu, idGhe, idHoaDon, giaBan, ngayBan)
    VALUES ('VE-01-A01', 1, 1, ?, 95000, '2026-11-01 10:15:00')
    ''', (hd1_id,))
    cursor.execute('''
    INSERT INTO tblVe (maVe, idLichChieu, idGhe, idHoaDon, giaBan, ngayBan)
    VALUES ('VE-01-A02', 1, 2, ?, 95000, '2026-11-01 10:15:00')
    ''', (hd1_id,))

    cursor.execute('''
    INSERT INTO tblHoaDon (maHD, idNhanVien, idKhachHang, ngayLap, tongTien, giamGia, thanhTien, phuongThucTT)
    VALUES ('HD-20261102-002', 2, 4, '2026-11-02 14:20:00', 260000, 18200, 241800, 'CHUYEN_KHOAN')
    ''')
    hd2_id = cursor.lastrowid
    cursor.execute('''
    INSERT INTO tblVe (maVe, idLichChieu, idGhe, idHoaDon, giaBan, ngayBan)
    VALUES ('VE-02-D04', 3, 28, ?, 125000, '2026-11-02 14:20:00')
    ''', (hd2_id,))
    cursor.execute('''
    INSERT INTO tblVe (maVe, idLichChieu, idGhe, idHoaDon, giaBan, ngayBan)
    VALUES ('VE-02-D05', 3, 29, ?, 125000, '2026-11-02 14:20:00')
    ''', (hd2_id,))

    # Mot don ban le khong the thanh vien
    cursor.execute('''
    INSERT INTO tblHoaDon (maHD, idNhanVien, idKhachHang, ngayLap, tongTien, giamGia, thanhTien, phuongThucTT)
    VALUES ('HD-20261103-003', 2, NULL, '2026-11-03 19:40:00', 105000, 0, 105000, 'TIEN_MAT')
    ''')
    hd3_id = cursor.lastrowid
    cursor.execute('''
    INSERT INTO tblVe (maVe, idLichChieu, idGhe, idHoaDon, giaBan, ngayBan)
    VALUES ('VE-03-B03', 1, 11, ?, 105000, '2026-11-03 19:40:00')
    ''', (hd3_id,))

if __name__ == '__main__':
    init_database()
