from dao.khach_hang_dao import KhachHangDAO

class KhachHangController:
    def __init__(self):
        self.kh_dao = KhachHangDAO()

    def dang_ky_thanh_vien(self, ho_ten: str, sdt: str, email: str, cccd: str, mat_khau: str, ngay_sinh: str, dia_chi: str = "") -> dict:
        # Validate co ban
        if not ho_ten or not sdt or not email or not cccd or not mat_khau:
            return {"success": False, "message": "Vui lòng điền đầy đủ các trường bắt buộc!"}

        if len(sdt) < 9 or len(sdt) > 12:
            return {"success": False, "message": "Số điện thoại không đúng định dạng!"}

        if "@" not in email:
            return {"success": False, "message": "Địa chỉ Email không hợp lệ!"}

        if self.kh_dao.kiem_tra_trung(sdt, email, cccd):
            return {"success": False, "message": "Số điện thoại, Email hoặc CCCD đã được đăng ký trên hệ thống!"}

        res = self.kh_dao.them_khach_hang(ho_ten, sdt, email, cccd, mat_khau, ngay_sinh, dia_chi)
        if res.get("success"):
            return {
                "success": True,
                "message": f"Chúc mừng quý khách {ho_ten} đã đăng ký thành viên thành công!",
                "data": res
            }
        else:
            return {"success": False, "message": f"Đăng ký thất bại: {res.get('error')}"}

    def tra_cuu_the(self, ma_the: str):
        if not ma_the:
            return None
        return self.kh_dao.tim_theo_ma_the(ma_the)

    def lay_danh_sach(self):
        return self.kh_dao.lay_tat_ca()
