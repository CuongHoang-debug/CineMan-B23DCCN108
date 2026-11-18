import hashlib
from dao.db_connection import DBConnection

class AuthController:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def dang_nhap(self, tai_khoan: str, mat_khau: str):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        hashed_pw = hashlib.sha256(mat_khau.encode('utf-8')).hexdigest()
        cursor.execute('''
        SELECT id, taiKhoan, hoTen, sdt, email, vaiTro
        FROM tblNguoiDung
        WHERE (taiKhoan = ? OR sdt = ? OR email = ?) AND matKhau = ?
        ''', (tai_khoan.strip(), tai_khoan.strip(), tai_khoan.strip(), hashed_pw))
        user = cursor.fetchone()
        conn.close()
        if user:
            return dict(user)
        return None
