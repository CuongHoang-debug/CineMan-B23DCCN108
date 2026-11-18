from dao.db_connection import DBConnection
from typing import List, Dict, Set

class GheDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def lay_ghe_theo_phong(self, id_phong: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM tblGhe
        WHERE idPhong = ?
        ORDER BY soHang ASC, soCot ASC
        ''', (id_phong,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def lay_ghe_da_dat(self, id_lich: int) -> Set[int]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT idGhe FROM tblVe
        WHERE idLichChieu = ? AND trangThai = 'DA_BAN'
        ''', (id_lich,))
        rows = cursor.fetchall()
        conn.close()
        return {r['idGhe'] for r in rows}

    def lay_so_do_ghe_va_trang_thai(self, id_lich: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Lay idPhong tu lich chieu
        cursor.execute("SELECT idPhong, giaVeGoc FROM tblLichChieu WHERE id = ?", (id_lich,))
        lich = cursor.fetchone()
        if not lich:
            conn.close()
            return []
        id_phong = lich['idPhong']
        gia_goc = lich['giaVeGoc']

        cursor.execute('''
        SELECT g.*,
               CASE WHEN v.id IS NOT NULL THEN 'DA_BAN' ELSE 'CON_TRONG' END as trangThaiDat,
               (? + g.phuThu) as giaVe
        FROM tblGhe g
        LEFT JOIN tblVe v ON g.id = v.idGhe AND v.idLichChieu = ? AND v.trangThai = 'DA_BAN'
        WHERE g.idPhong = ?
        ORDER BY g.soHang ASC, g.soCot ASC
        ''', (gia_goc, id_lich, id_phong))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
