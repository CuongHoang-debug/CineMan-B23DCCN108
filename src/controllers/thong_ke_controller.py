from dao.thong_ke_dao import ThongKeDAO

class ThongKeController:
    def __init__(self):
        self.tk_dao = ThongKeDAO()

    def lay_thong_ke_tong_quan(self):
        return self.tk_dao.thong_ke_tong_quan()

    def lay_thong_ke_phim(self):
        return self.tk_dao.thong_ke_phim()

    def lay_thong_ke_khach_hang(self):
        return self.tk_dao.thong_ke_khach_hang()

    def lay_thong_ke_doanh_thu(self):
        return self.tk_dao.thong_ke_doanh_thu_theo_ngay()
