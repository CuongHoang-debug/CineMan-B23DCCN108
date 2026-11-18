from dao.db_connection import DBConnection
from typing import List, Dict, Optional

class LichChieuDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def lay_lich_theo_phim(self, id_phim: int, ngay: Optional[str] = None) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = '''
        SELECT lc.*, p.tenPhim, p.thoiLuong, pc.tenPhong, pc.loaiPhong
        FROM tblLichChieu lc
        JOIN tblPhim p ON lc.idPhim = p.id
        JOIN tblPhongChieu pc ON lc.idPhong = pc.id
        WHERE lc.idPhim = ?
        '''
        params = [id_phim]
        if ngay:
            sql += " AND lc.ngayChieu = ?"
            params.append(ngay)
        sql += " ORDER BY lc.ngayChieu ASC, lc.gioBatDau ASC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def lay_theo_id(self, id_lich: int) -> Optional[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT lc.*, p.tenPhim, p.thoiLuong, p.poster, p.doTuoi, pc.tenPhong, pc.loaiPhong
        FROM tblLichChieu lc
        JOIN tblPhim p ON lc.idPhim = p.id
        JOIN tblPhongChieu pc ON lc.idPhong = pc.id
        WHERE lc.id = ?
        ''', (id_lich,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def them_lich_chieu(self, id_phim: int, id_phong: int, ngay_chieu: str, gio_bat_dau: str, gio_ket_thuc: str, gia_ve_goc: float) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO tblLichChieu (idPhim, idPhong, ngayChieu, gioBatDau, gioKetThuc, giaVeGoc)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_phim, id_phong, ngay_chieu, gio_bat_dau, gio_ket_thuc, gia_ve_goc))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def lay_tat_ca_lich(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT lc.*, p.tenPhim, pc.tenPhong, pc.loaiPhong
        FROM tblLichChieu lc
        JOIN tblPhim p ON lc.idPhim = p.id
        JOIN tblPhongChieu pc ON lc.idPhong = pc.id
        ORDER BY lc.ngayChieu DESC, lc.gioBatDau ASC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
