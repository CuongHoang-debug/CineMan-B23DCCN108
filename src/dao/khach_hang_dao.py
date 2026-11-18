import hashlib
import random
from dao.db_connection import DBConnection
from models.entities import KhachHang, TheThanhVien

class KhachHangDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def kiem_tra_trung(self, sdt: str, email: str, cccd: str) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT u.id FROM tblNguoiDung u
        LEFT JOIN tblKhachHang k ON u.id = k.id
        WHERE u.sdt = ? OR u.email = ? OR k.cccd = ?
        ''', (sdt, email, cccd))
        row = cursor.fetchone()
        conn.close()
        return row is not None

    def them_khach_hang(self, ho_ten: str, sdt: str, email: str, cccd: str, mat_khau: str, ngay_sinh: str, dia_chi: str = "") -> dict:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN TRANSACTION;")
            hashed_pw = hashlib.sha256(mat_khau.encode('utf-8')).hexdigest()
            tai_khoan = sdt # mac dinh lay sdt lam ten dang nhap

            cursor.execute('''
            INSERT INTO tblNguoiDung (taiKhoan, matKhau, hoTen, sdt, email, vaiTro)
            VALUES (?, ?, ?, ?, ?, 'KHACH_HANG')
            ''', (tai_khoan, hashed_pw, ho_ten, sdt, email))
            user_id = cursor.lastrowid

            cursor.execute('''
            INSERT INTO tblKhachHang (id, cccd, ngaySinh, diaChi)
            VALUES (?, ?, ?, ?)
            ''', (user_id, cccd, ngay_sinh, dia_chi))

            # Tu dong sinh ma the thanh vien
            ma_the = f"MB-{random.randint(1000, 9999)}"
            cursor.execute('''
            INSERT INTO tblTheThanhVien (maThe, idKhachHang, hangThe, diemTichLuy)
            VALUES (?, ?, 'Standard', 0)
            ''', (ma_the, user_id))

            conn.commit()
            return {
                "success": True,
                "user_id": user_id,
                "ho_ten": ho_ten,
                "ma_the": ma_the,
                "hang_the": "Standard",
                "diem": 0
            }
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def tim_theo_ma_the(self, ma_the: str):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT t.id as idThe, t.maThe, t.hangThe, t.diemTichLuy,
               u.id as idND, u.hoTen, u.sdt, u.email, k.cccd
        FROM tblTheThanhVien t
        JOIN tblKhachHang k ON t.idKhachHang = k.id
        JOIN tblNguoiDung u ON k.id = u.id
        WHERE UPPER(t.maThe) = UPPER(?)
        ''', (ma_the.strip(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    def cap_nhat_diem(self, ma_the: str, diem_cong: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE tblTheThanhVien
            SET diemTichLuy = diemTichLuy + ?
            WHERE UPPER(maThe) = UPPER(?)
            ''', (diem_cong, ma_the.strip()))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def lay_tat_ca(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT u.id, u.hoTen, u.sdt, u.email, k.cccd, t.maThe, t.hangThe, t.diemTichLuy
        FROM tblKhachHang k
        JOIN tblNguoiDung u ON k.id = u.id
        LEFT JOIN tblTheThanhVien t ON k.id = t.idKhachHang
        ORDER BY u.id DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
