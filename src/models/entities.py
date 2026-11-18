from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class NguoiDung:
    id: int = 0
    taiKhoan: str = ""
    matKhau: str = ""
    hoTen: str = ""
    sdt: str = ""
    email: str = ""
    vaiTro: str = "" # 'QUAN_LY', 'BAN_HANG', 'KHACH_HANG'
    ngayTao: str = ""

@dataclass
class NhanVien(NguoiDung):
    chucVu: str = ""
    caLamViec: str = ""
    luongCoBan: float = 0.0

@dataclass
class TheThanhVien:
    id: int = 0
    maThe: str = ""
    idKhachHang: int = 0
    hangThe: str = "Standard" # 'Standard', 'Silver', 'Gold', 'VIP'
    diemTichLuy: int = 0
    ngayCap: str = ""
    trangThai: str = "HOAT_DONG"

@dataclass
class KhachHang(NguoiDung):
    cccd: str = ""
    ngaySinh: str = ""
    diaChi: str = ""
    theThanhVien: Optional[TheThanhVien] = None

@dataclass
class Phim:
    id: int = 0
    tenPhim: str = ""
    theLoai: str = ""
    thoiLuong: int = 0
    daoDien: str = ""
    dienVien: str = ""
    doTuoi: str = "P"
    poster: str = ""
    moTa: str = ""
    trangThai: str = "DANG_CHIEU"

@dataclass
class Ghe:
    id: int = 0
    idPhong: int = 0
    maGhe: str = ""
    soHang: str = ""
    soCot: int = 0
    loaiGhe: str = "THUONG" # 'THUONG', 'VIP', 'SWEETBOX'
    phuThu: float = 0.0

@dataclass
class PhongChieu:
    id: int = 0
    tenPhong: str = ""
    loaiPhong: str = "2D"
    tongSoGhe: int = 0
    danhSachGhe: List[Ghe] = field(default_factory=list)

@dataclass
class LichChieu:
    id: int = 0
    idPhim: int = 0
    idPhong: int = 0
    ngayChieu: str = ""
    gioBatDau: str = ""
    gioKetThuc: str = ""
    giaVeGoc: float = 0.0
    phim: Optional[Phim] = None
    phongChieu: Optional[PhongChieu] = None

@dataclass
class Ve:
    id: int = 0
    maVe: str = ""
    idLichChieu: int = 0
    idGhe: int = 0
    idHoaDon: int = 0
    giaBan: float = 0.0
    ngayBan: str = ""
    trangThai: str = "DA_BAN"
    ghe: Optional[Ghe] = None
    lichChieu: Optional[LichChieu] = None

@dataclass
class HoaDon:
    id: int = 0
    maHD: str = ""
    idNhanVien: int = 0
    idKhachHang: Optional[int] = None
    ngayLap: str = ""
    tongTien: float = 0.0
    giamGia: float = 0.0
    thanhTien: float = 0.0
    phuongThucTT: str = "TIEN_MAT"
    danhSachVe: List[Ve] = field(default_factory=list)
    nhanVien: Optional[NhanVien] = None
    khachHang: Optional[KhachHang] = None
