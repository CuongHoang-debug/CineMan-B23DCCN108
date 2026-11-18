from dao.db_connection import DBConnection
from typing import Dict, List, Any

class ThongKeDAO:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def thong_ke_tong_quan(self) -> Dict[str, Any]:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Tong doanh thu
        cursor.execute("SELECT COALESCE(SUM(thanhTien), 0) FROM tblHoaDon")
        tong_doanh_thu = cursor.fetchone()[0]

        # Tong so ve da ban
        cursor.execute("SELECT COUNT(*) FROM tblVe WHERE trangThai = 'DA_BAN'")
        tong_so_ve = cursor.fetchone()[0]

        # Tong so khach hang
        cursor.execute("SELECT COUNT(*) FROM tblKhachHang")
        tong_khach_hang = cursor.fetchone()[0]

        # Tong so phim dang chieu
        cursor.execute("SELECT COUNT(*) FROM tblPhim WHERE trangThai = 'DANG_CHIEU'")
        tong_phim = cursor.fetchone()[0]

        conn.close()
        return {
            "tong_doanh_thu": tong_doanh_thu,
            "tong_so_ve": tong_so_ve,
            "tong_khach_hang": tong_khach_hang,
            "tong_phim": tong_phim
        }

    def thong_ke_phim(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT p.id, p.tenPhim, p.theLoai, p.thoiLuong,
               COUNT(v.id) as soVeDaBan,
               COALESCE(SUM(v.giaBan), 0) as doanhThuPhim
        FROM tblPhim p
        LEFT JOIN tblLichChieu lc ON p.id = lc.idPhim
        LEFT JOIN tblVe v ON lc.id = v.idLichChieu AND v.trangThai = 'DA_BAN'
        GROUP BY p.id
        ORDER BY doanhThuPhim DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def thong_ke_khach_hang(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT u.id, u.hoTen, u.sdt, u.email,
               t.maThe, t.hangThe, t.diemTichLuy,
               COUNT(DISTINCT hd.id) as soLanMua,
               COALESCE(SUM(hd.thanhTien), 0) as tongChiTieu
        FROM tblKhachHang kh
        JOIN tblNguoiDung u ON kh.id = u.id
        LEFT JOIN tblTheThanhVien t ON kh.id = t.idKhachHang
        LEFT JOIN tblHoaDon hd ON kh.id = hd.idKhachHang
        GROUP BY kh.id
        ORDER BY tongChiTieu DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def thong_ke_doanh_thu_theo_ngay(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT strftime('%Y-%m-%d', ngayLap) as ngay,
               COUNT(id) as soHoaDon,
               SUM(thanhTien) as doanhThuNgay
        FROM tblHoaDon
        GROUP BY ngay
        ORDER BY ngay DESC
        LIMIT 10
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
