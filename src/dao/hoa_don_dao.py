import uuid
from datetime import datetime
from dao.db_connection import DBConnection
from typing import List, Dict, Optional

class HoaDonDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def tao_hoa_don(self, id_nhan_vien: int, id_khach_hang: Optional[int], tong_tien: float, giam_gia: float, thanh_tien: float, phuong_thuc_tt: str = 'TIEN_MAT') -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        ma_hd = f"HD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        cursor.execute('''
        INSERT INTO tblHoaDon (maHD, idNhanVien, idKhachHang, ngayLap, tongTien, giamGia, thanhTien, phuongThucTT)
        VALUES (?, ?, ?, datetime('now', 'localtime'), ?, ?, ?, ?)
        ''', (ma_hd, id_nhan_vien, id_khach_hang, tong_tien, giam_gia, thanh_tien, phuong_thuc_tt))
        hd_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return hd_id

    def lay_chi_tiet(self, id_hd: int) -> Optional[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT hd.*,
               nvU.hoTen as tenNhanVien,
               khU.hoTen as tenKhachHang, khU.sdt as sdtKhachHang,
               t.maThe, t.hangThe
        FROM tblHoaDon hd
        JOIN tblNhanVien nv ON hd.idNhanVien = nv.id
        JOIN tblNguoiDung nvU ON nv.id = nvU.id
        LEFT JOIN tblKhachHang kh ON hd.idKhachHang = kh.id
        LEFT JOIN tblNguoiDung khU ON kh.id = khU.id
        LEFT JOIN tblTheThanhVien t ON kh.id = t.idKhachHang
        WHERE hd.id = ?
        ''', (id_hd,))
        hd = cursor.fetchone()
        if not hd:
            conn.close()
            return None

        # Lay danh sach ve trong hoa don
        cursor.execute('''
        SELECT v.*, g.maGhe, g.soHang, g.soCot, g.loaiGhe,
               lc.ngayChieu, lc.gioBatDau, lc.gioKetThuc,
               p.tenPhim, p.doTuoi, pc.tenPhong, pc.loaiPhong
        FROM tblVe v
        JOIN tblGhe g ON v.idGhe = g.id
        JOIN tblLichChieu lc ON v.idLichChieu = lc.id
        JOIN tblPhim p ON lc.idPhim = p.id
        JOIN tblPhongChieu pc ON lc.idPhong = pc.id
        WHERE v.idHoaDon = ?
        ''', (id_hd,))
        ves = cursor.fetchall()
        conn.close()

        res = dict(hd)
        res['danhSachVe'] = [dict(v) for v in ves]
        return res
