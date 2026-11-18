from dao.db_connection import DBConnection
from typing import List, Dict, Optional

class PhimDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def tim_phim(self, tu_khoa: str = "") -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        if tu_khoa.strip():
            cursor.execute('''
            SELECT * FROM tblPhim
            WHERE tenPhim LIKE ? OR theLoai LIKE ?
            ORDER BY id DESC
            ''', (f"%{tu_khoa.strip()}%", f"%{tu_khoa.strip()}%"))
        else:
            cursor.execute("SELECT * FROM tblPhim ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def lay_phim_theo_id(self, id_phim: int) -> Optional[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblPhim WHERE id = ?", (id_phim,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def them_phim(self, ten_phim: str, the_loai: str, thoi_luong: int, dao_dien: str, dien_vien: str, do_tuoi: str, poster: str, mo_ta: str) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO tblPhim (tenPhim, theLoai, thoiLuong, daoDien, dienVien, doTuoi, poster, moTa, trangThai)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'DANG_CHIEU')
            ''', (ten_phim, the_loai, thoi_luong, dao_dien, dien_vien, do_tuoi, poster, mo_ta))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def sua_phim(self, id_phim: int, ten_phim: str, the_loai: str, thoi_luong: int, dao_dien: str, dien_vien: str, do_tuoi: str, poster: str, mo_ta: str, trang_thai: str) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE tblPhim
            SET tenPhim = ?, theLoai = ?, thoiLuong = ?, daoDien = ?, dienVien = ?, doTuoi = ?, poster = ?, moTa = ?, trangThai = ?
            WHERE id = ?
            ''', (ten_phim, the_loai, thoi_luong, dao_dien, dien_vien, do_tuoi, poster, mo_ta, trang_thai, id_phim))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def xoa_phim(self, id_phim: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tblPhim WHERE id = ?", (id_phim,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
