import uuid
from datetime import datetime
from dao.db_connection import DBConnection
from typing import List, Dict

class VeDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def tao_ve(self, id_lich: int, id_ghe: int, id_hoa_don: int, gia_ban: float) -> str:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        ma_ve = f"TICK-{datetime.now().strftime('%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        cursor.execute('''
        INSERT INTO tblVe (maVe, idLichChieu, idGhe, idHoaDon, giaBan, ngayBan, trangThai)
        VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), 'DA_BAN')
        ''', (ma_ve, id_lich, id_ghe, id_hoa_don, gia_ban))
        conn.commit()
        conn.close()
        return ma_ve
