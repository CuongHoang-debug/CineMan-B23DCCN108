from dao.phim_dao import PhimDAO
from dao.lich_chieu_dao import LichChieuDAO
from dao.ghe_dao import GheDAO
from dao.khach_hang_dao import KhachHangDAO
from dao.hoa_don_dao import HoaDonDAO
from dao.ve_dao import VeDAO
from typing import List, Dict, Optional

class BanVeController:
    def __init__(self):
        self.phim_dao = PhimDAO()
        self.lich_dao = LichChieuDAO()
        self.ghe_dao = GheDAO()
        self.kh_dao = KhachHangDAO()
        self.hd_dao = HoaDonDAO()
        self.ve_dao = VeDAO()

    def tim_kiem_phim(self, tu_khoa: str = ""):
        return self.phim_dao.tim_phim(tu_khoa)

    def chon_phim(self, id_phim: int, ngay: Optional[str] = None):
        phim = self.phim_dao.lay_phim_theo_id(id_phim)
        lich_chieu = self.lich_dao.lay_lich_theo_phim(id_phim, ngay)
        return {"phim": phim, "danh_sach_suat_chieu": lich_chieu}

    def chon_suat_chieu(self, id_lich: int):
        lich = self.lich_dao.lay_theo_id(id_lich)
        so_do_ghe = self.ghe_dao.lay_so_do_ghe_va_trang_thai(id_lich)
        return {"lich_chieu": lich, "so_do_ghe": so_do_ghe}

    def tinh_tien(self, id_lich: int, ds_id_ghe: List[int], ma_the: Optional[str] = None) -> Dict:
        so_do = self.ghe_dao.lay_so_do_ghe_va_trang_thai(id_lich)
        ghe_dict = {g['id']: g for g in so_do}

        tong_tien_goc = 0.0
        danh_sach_ghe_chon = []

        for gid in ds_id_ghe:
            if gid in ghe_dict:
                g = ghe_dict[gid]
                tong_tien_goc += g['giaVe']
                danh_sach_ghe_chon.append(g)

        ti_le_giam = 0.0
        thong_tin_the = None

        if ma_the and ma_the.strip():
            thong_tin_the = self.kh_dao.tim_theo_ma_the(ma_the.strip())
            if thong_tin_the:
                hang = thong_tin_the.get('hangThe', 'Standard')
                if hang == 'VIP':
                    ti_le_giam = 0.15
                elif hang == 'Gold':
                    ti_le_giam = 0.10
                elif hang == 'Silver':
                    ti_le_giam = 0.07
                else:
                    ti_le_giam = 0.05

        so_tien_giam = tong_tien_goc * ti_le_giam
        thanh_tien = max(0.0, tong_tien_goc - so_tien_giam)
        diem_tich_luy_moi = int(thanh_tien // 10000) # 10.000d = 1 diem

        return {
            "tong_tien_goc": tong_tien_goc,
            "ti_le_giam": ti_le_giam,
            "so_tien_giam": so_tien_giam,
            "thanh_tien": thanh_tien,
            "thong_tin_the": thong_tin_the,
            "diem_tich_luy_cong": diem_tich_luy_moi,
            "so_luong_ve": len(danh_sach_ghe_chon),
            "danh_sach_ghe": danh_sach_ghe_chon
        }

    def xac_nhan_thanh_toan(self, id_lich: int, ds_id_ghe: List[int], id_nhan_vien: int, ma_the: Optional[str] = None, phuong_thuc_tt: str = 'TIEN_MAT') -> Dict:
        if not ds_id_ghe:
            return {"success": False, "message": "Chưa chọn ghế nào!"}

        # Kiem tra trung ghe
        ghe_da_dat = self.ghe_dao.lay_ghe_da_dat(id_lich)
        for gid in ds_id_ghe:
            if gid in ghe_da_dat:
                return {"success": False, "message": f"Ghế có mã ID {gid} vừa có người đặt trước, vui lòng chọn lại!"}

        calc = self.tinh_tien(id_lich, ds_id_ghe, ma_the)
        id_khach_hang = None
        if calc["thong_tin_the"]:
            id_khach_hang = calc["thong_tin_the"]["idND"]

        # 1. Tao Hoa Don
        hd_id = self.hd_dao.tao_hoa_don(
            id_nhan_vien=id_nhan_vien,
            id_khach_hang=id_khach_hang,
            tong_tien=calc["tong_tien_goc"],
            giam_gia=calc["so_tien_giam"],
            thanh_tien=calc["thanh_tien"],
            phuong_thuc_tt=phuong_thuc_tt
        )

        # 2. Tao Ve cho tung ghe
        ma_ves = []
        for g in calc["danh_sach_ghe"]:
            ma_ve = self.ve_dao.tao_ve(
                id_lich=id_lich,
                id_ghe=g["id"],
                id_hoa_don=hd_id,
                gia_ban=g["giaVe"]
            )
            ma_ves.append(ma_ve)

        # 3. Tich diem neu co the
        if ma_the and calc["thong_tin_the"]:
            self.kh_dao.cap_nhat_diem(ma_the, calc["diem_tich_luy_cong"])

        # 4. Lay day du chi tiet hoa don de in
        hoa_don_detail = self.hd_dao.lay_chi_tiet(hd_id)

        return {
            "success": True,
            "message": "Thanh toán và xuất vé thành công!",
            "hoa_don_id": hd_id,
            "hoa_don": hoa_don_detail
        }
