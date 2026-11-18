from dao.db_connection import DBConnection
from typing import List, Dict

class PhongChieuDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def lay_tat_ca(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblPhongChieu ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def lay_theo_id(self, id_phong: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblPhongChieu WHERE id = ?", (id_phong,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
