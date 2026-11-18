from dao.phim_dao import PhimDAO
from dao.phong_chieu_dao import PhongChieuDAO
from dao.lich_chieu_dao import LichChieuDAO

class PhimController:
    def __init__(self):
        self.phim_dao = PhimDAO()
        self.phong_dao = PhongChieuDAO()
        self.lich_dao = LichChieuDAO()

    def lay_danh_sach(self, tu_khoa=""):
        return self.phim_dao.tim_phim(tu_khoa)

    def them_phim(self, ten_phim, the_loai, thoi_luong, dao_dien, dien_vien, do_tuoi, poster, mo_ta):
        return self.phim_dao.them_phim(ten_phim, the_loai, int(thoi_luong), dao_dien, dien_vien, do_tuoi, poster, mo_ta)

    def sua_phim(self, id_phim, ten_phim, the_loai, thoi_luong, dao_dien, dien_vien, do_tuoi, poster, mo_ta, trang_thai):
        return self.phim_dao.sua_phim(int(id_phim), ten_phim, the_loai, int(thoi_luong), dao_dien, dien_vien, do_tuoi, poster, mo_ta, trang_thai)

    def xoa_phim(self, id_phim):
        return self.phim_dao.xoa_phim(int(id_phim))

    def lay_phong_chieu(self):
        return self.phong_dao.lay_tat_ca()

    def tao_lich_chieu(self, id_phim, id_phong, ngay_chieu, gio_bat_dau, gio_ket_thuc, gia_ve_goc):
        return self.lich_dao.them_lich_chieu(int(id_phim), int(id_phong), ngay_chieu, gio_bat_dau, gio_ket_thuc, float(gia_ve_goc))

    def lay_tat_ca_lich(self):
        return self.lich_dao.lay_tat_ca_lich()
