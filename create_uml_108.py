import os

uml_dir = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\uml_108"

# 1. Use Case Tong Quan
uc_tongquan = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam actorStyle awesome

actor "Thành viên hệ thống" as TV
actor "Nhân viên" as NV
actor "Nhân viên quản lý" as NVQL
actor "Nhân viên bán hàng" as NVBH
actor "Khách hàng" as KH

NV -up-|> TV
NVQL -up-|> NV
NVBH -up-|> NV
KH -up-|> TV

rectangle "Hệ thống quản lý rạp chiếu phim CineMan" {
    usecase "Đăng nhập 108" as UC_Login
    usecase "Đổi mật khẩu 108" as UC_Pass
    usecase "Đăng xuất 108" as UC_Logout
    usecase "Xem thống kê 108" as UC_ThongKe
    usecase "Quản lý thông tin phim 108" as UC_QLPhim
    usecase "Thêm thông tin phim 108" as UC_ThemPhim
    usecase "Quản lý phòng chiếu 108" as UC_QLPhong
    usecase "Quản lý lịch chiếu phim 108" as UC_QLLich
    usecase "Tìm kiếm phim 108" as UC_TimPhim
    usecase "Mua vé trực tuyến 108" as UC_MuaVeOnline
    usecase "Bán vé tại quầy 108" as UC_BanVe
    usecase "Xuất thẻ thành viên 108" as UC_XuatThe
    usecase "Đăng ký thành viên 108" as UC_DangKy
}

TV --> UC_Login
TV --> UC_Pass
TV --> UC_Logout

NVQL --> UC_ThongKe
NVQL --> UC_QLPhim
NVQL --> UC_QLPhong
NVQL --> UC_QLLich

NVBH --> UC_BanVe
NVBH --> UC_XuatThe

KH --> UC_TimPhim
KH --> UC_MuaVeOnline
KH --> UC_DangKy

UC_ThemPhim .up.> UC_QLPhim : <<Extend>>
@enduml
"""

# 2. Use Case Chi Tiet: Dang ky thanh vien
uc_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam actorStyle awesome

actor "Khách hàng" as KH

rectangle "Phân hệ Đăng ký thành viên" {
    usecase "Đăng ký thành viên 108" as UC_DK
    usecase "Nhập thông tin cá nhân 108" as UC_NhapTT
    usecase "Lưu CSDL & Cấp thẻ 108" as UC_CapThe
}

KH --> UC_DK
UC_DK ..> UC_NhapTT : <<Include>>
UC_DK ..> UC_CapThe : <<Include>>
@enduml
"""

# 3. Use Case Chi Tiet: Ban ve tai quay
uc_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam actorStyle awesome

actor "Thành viên hệ thống" as TV
actor "Nhân viên bán hàng" as NVBH
actor "Khách hàng" as KH

NVBH -up-|> TV

rectangle "Phân hệ Bán vé tại quầy" {
    usecase "Đăng nhập 108" as UC_Login
    usecase "Bán vé tại quầy 108" as UC_BV
    usecase "chọn phim 108" as UC_Phim
    usecase "chọn giờ 108" as UC_Gio
    usecase "chọn ghế 108" as UC_Ghe
    usecase "nhập mã khách hàng 108" as UC_MaKH
    usecase "thanh toán 108" as UC_TT
}

NVBH --> UC_BV
KH --> UC_BV

UC_BV ..> UC_Login : <<Include>>
UC_BV ..> UC_Phim : <<Include>>
UC_BV ..> UC_Gio : <<Include>>
UC_BV ..> UC_Ghe : <<Include>>
UC_BV ..> UC_TT : <<Include>>
UC_MaKH .up.> UC_BV : <<Extend>>
@enduml
"""

# 4. Entity Class Diagram (Giong het trang 18 & 27 PDF)
entity_diagram = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam classAttributeIconSize 0

class Hoten108 {
    -ho: String
    -tendem: String
    -ten: String
}

class Thanhvien108 {
    -id: int
    -username: String
    -password: String
    -name: String
    -ngaysinh: date
    -diachi: String
    -email: String
    -sdt: String
    -ghichu: String
}

class Nhanvien108 {
    -chucVu: String
}

class NVQuanLy108 {
}

class NVBanHang108 {
}

class Khachhang108 {
}

class Thethanhvien108 {
    -id: int
    -maso: String
    -ngaycap: date
    -ngayhethan: date
}

class Rapchieuphim108 {
    -id: int
    -tenrap: String
    -sophongchieu: int
}

class Phongchieu108 {
    -id: int
    -maso: String
    -succhua: int
}

class Ghe108 {
    -id: int
    -maghe: String
    -trangthai: boolean
}

class Phim108 {
    -id: int
    -tenphim: String
    -theloai: String
    -daodien: String
    -mota: String
    -thoiluong: int
}

class Suatchieu108 {
    -id: int
    -tgbatdau: dateTime
    -tgketthuc: dateTime
    -ngaychieu: date
    -giochieu: dateTime
}

class Hoadon108 {
    -id: int
    -mahoadon: String
    -ngay: date
    -tongtien: Float
    -trangthai: boolean
}

class Ve108 {
    -id: int
    -mave: String
}

class TKDoanhthu108 {
    -tongdoanhthu: float
}

class TKKhachhang108 {
    -tongsokhachhang: int
}

Thanhvien108 *-- Hoten108
Nhanvien108 --|> Thanhvien108
Khachhang108 --|> Thanhvien108
NVQuanLy108 --|> Nhanvien108
NVBanHang108 --|> Nhanvien108

Khachhang108 "1" -- "0..1" Thethanhvien108
Rapchieuphim108 "1" *-- "1..*" Phongchieu108
Phongchieu108 "1" *-- "1..*" Ghe108
Phim108 "1" -- "0..*" Suatchieu108
Phongchieu108 "1" -- "0..*" Suatchieu108

Suatchieu108 "1" -- "0..*" Ve108
Ghe108 "1" -- "0..*" Ve108
Hoadon108 "1" *-- "1..*" Ve108

Hoadon108 --|> TKDoanhthu108
Khachhang108 --|> TKKhachhang108

NVBanHang108 "1" -- "0..*" Hoadon108
Khachhang108 "1" -- "0..*" Hoadon108
@enduml
"""

# 5. Analysis Class Diagram cho Module Ban ve (Trang 21 PDF)
analysis_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam classAttributeIconSize 0

class GDChinhNVBH108 <<boundary>> {
    -subBanVe: submit
}

class GDChonPhim108 <<boundary>> {
    -moutChonPhim: in/out
    -moutChonSuatChieu: in/out
    -subTiepTuc: submit
}

class GDChonSuatChieu108 <<boundary>> {
    -outTenPhim: output
    -moutChonSuatChieu: in/out
    -subTiepTuc: submit
}

class GDChonGhe108 <<boundary>> {
    -moutDanhSachGhe: in/out
    -subTiepTuc: submit
}

class GDThanhToan108 <<boundary>> {
    -outThongTinVe: output
    -inPhuongThucThanhToan: input
    -inNhapMathethanhvien: input
    -subThanhToan: submit
}

class Phim108 <<entity>> {
    -tenphim: String
    -theloai: String
    -daodien: String
    -thoiluong: int
    -mota: String
    +getphim()
}

class Suatchieu108 <<entity>> {
    -tgbatdau: dateTime
    -tgketthuc: dateTime
    -ngaychieu: date
    -giochieu: dateTime
    +getsuatchieu()
}

class Ghe108 <<entity>> {
    -maghe: String
    -trangthai: boolean
    +getghetrong()
}

class Hoadon108 <<entity>> {
    -mahoadon: String
    -ngay: date
    -tongtien: float
    -trangthai: boolean
    +getTTHoaDon()
    +ThanhToan()
    +luuHoaDon()
}

class Ve108 <<entity>> {
    -mave: String
}

class Thethanhvien108 <<entity>> {
    -mathe: String
    -cappdo: String
    -diem: int
}

class Khachhang108 <<entity>> {
}

GDChinhNVBH108 ..> GDChonPhim108
GDChonPhim108 ..> GDChonSuatChieu108
GDChonSuatChieu108 ..> GDChonGhe108
GDChonGhe108 ..> GDThanhToan108

GDChonPhim108 ..> Phim108 : getphim()
GDChonSuatChieu108 ..> Suatchieu108 : getsuatchieu()
GDChonGhe108 ..> Ghe108 : getghetrong()
GDThanhToan108 ..> Hoadon108 : ThanhToan()

Phim108 "1" -- "0..*" Suatchieu108
Suatchieu108 "1" -- "0..*" Ve108
Ghe108 "1" -- "0..*" Ve108
Hoadon108 "1" *-- "1..*" Ve108
Khachhang108 "1" -- "0..1" Thethanhvien108
Thethanhvien108 ..> GDThanhToan108
@enduml
"""

# 6. Communication Diagram Module Ban ve (Trang 25 PDF)
comm_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false

actor "Nhân viên / Khách hàng" as Actor
boundary "GDChinhNVBH108" as GDChinh
boundary "GDChonPhim108" as GDPhim
boundary "GDChonSuatChieu108" as GDLich
boundary "GDChonGhe108" as GDGhe
boundary "GDThanhToan108" as GDTT

entity "Phim108" as EPhim
entity "Suatchieu108" as ELich
entity "Ghe108" as EGhe
entity "Hoadon108" as EHD

Actor -> GDChinh : 1: Click bán vé
GDChinh -> GDPhim : 2: Gọi
GDPhim -> EPhim : 3: Gọi\n4: getphim()
EPhim -> GDPhim : 5: Trả về
GDPhim -> Actor : 6: Hiển thị
Actor -> GDPhim : 7: Click chọn

GDPhim -> GDLich : 8: Gọi
GDLich -> ELich : 9: Gọi\n10: getSuatChieu()
ELich -> GDLich : 11: Trả về
GDLich -> Actor : 12: Hiển thị
Actor -> GDLich : 13: Click chọn

GDLich -> GDGhe : 14: Gọi
GDGhe -> EGhe : 15: Gọi\n16: getghetrong()
EGhe -> GDGhe : 17: Trả về
GDGhe -> Actor : 18: Hiển thị
Actor -> GDGhe : 19: Click chọn

GDGhe -> GDTT : 20: Gọi
GDTT -> EHD : 21: Gọi\n22: getTTHoaDon()
EHD -> GDTT : 23: Trả về
GDTT -> Actor : 24: Hiển thị
Actor -> GDTT : 25: Click thanh toán
GDTT -> EHD : 26: Gọi\n27: ThanhToan(), luuHoaDon()
EHD -> GDTT : 28: Trả về
GDTT -> Actor : 29: Thông báo thành công
@enduml
"""

# 7. Sequence Analysis Ban ve (Trang 26 PDF)
seq_analysis_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam sequenceMessageAlign center

actor "Nhân viên / Khách" as Actor
boundary "GDChinhNVBH108" as GD0
boundary "GDChonPhim108" as GD1
entity "Phim108" as E1
boundary "GDChonSuatChieu108" as GD2
entity "Suatchieu108" as E2
boundary "GDChonGhe108" as GD3
entity "Ghe108" as E3
boundary "GDThanhToan108" as GD4
entity "Hoadon108" as E4

Actor -> GD0 : 1: Click bán vé
activate GD0
GD0 -> GD1 : 2: Gọi
activate GD1
GD1 -> E1 : 3: Gọi
activate E1
E1 -> E1 : 4: getphim()
E1 --> GD1 : 5: Trả về
deactivate E1
GD1 --> Actor : 6: Hiển thị
Actor -> GD1 : 7: Click chọn

GD1 -> GD2 : 8: Gọi
activate GD2
GD2 -> E2 : 9: Gọi
activate E2
E2 -> E2 : 10: getSuatChieu()
E2 --> GD2 : 11: Trả về
deactivate E2
GD2 --> Actor : 12: Hiển thị
Actor -> GD2 : 13: Click chọn

GD2 -> GD3 : 14: Gọi
activate GD3
GD3 -> E3 : 15: Gọi
activate E3
E3 -> E3 : 16: getghetrong()
E3 --> GD3 : 17: Trả về
deactivate E3
GD3 --> Actor : 18: Hiển thị
Actor -> GD3 : 19: Click chọn

GD3 -> GD4 : 20: Gọi
activate GD4
GD4 -> E4 : 21: Gọi
activate E4
E4 -> E4 : 22: getTTHoaDon()
E4 --> GD4 : 23: Trả về
deactivate E4
GD4 --> Actor : 24: Hiển thị
Actor -> GD4 : 25: Click thanh toán
GD4 -> E4 : 26: Gọi
activate E4
E4 -> E4 : 27: ThanhToan(), luuHoaDon()
E4 --> GD4 : 28: Trả về
deactivate E4
GD4 --> Actor : 29: Thông báo thành công
deactivate GD4
deactivate GD3
deactivate GD2
deactivate GD1
deactivate GD0
@enduml
"""

# 8. Database Schema (Trang 28 PDF)
db_schema = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam linetype ortho

entity "tblThanhVien108" as tblThanhVien {
    * id : int <<PK>>
    --
    username : varchar(255)
    password : varchar(255)
    ngaySinh : date
    diaChi : varchar(255)
    email : varchar(255)
    sdt : varchar(255)
    ghiChu : varchar(255)
    tblHoTen108id : int <<FK>>
}

entity "tblHoTen108" as tblHoTen {
    * id : int <<PK>>
    --
    ho : varchar(255)
    tenDem : varchar(255)
    ten : varchar(255)
}

entity "tblKhachHang108" as tblKhachHang {
    * id : int <<PK>>
    --
    maSo : varchar(255)
    tblThanhVien108id : int <<FK>>
}

entity "tblTheThanhVien108" as tblTheThanhVien {
    * id : int <<PK>>
    --
    maThe : varchar(255)
    ngayCap : date
    ngayHetHan : date
    diemTichLuy : int
    tblKhachHang108id : int <<FK>>
}

entity "tblPhim108" as tblPhim {
    * id : int <<PK>>
    --
    ten : varchar(255)
    theLoai : varchar(255)
    daoDien : varchar(255)
    moTa : varchar(255)
    thoiLuong : int
}

entity "tblPhongChieu108" as tblPhongChieu {
    * id : int <<PK>>
    --
    maSo : varchar(255)
    sucChua : int
    tblRapChieu472id : int
}

entity "tblGhe108" as tblGhe {
    * id : int <<PK>>
    --
    maGhe : varchar(255)
    trangThai : int
    tblPhongChieu108id : int <<FK>>
}

entity "tblSuatChieu108" as tblSuatChieu {
    * id : int <<PK>>
    --
    batDau : time
    ketThuc : time
    ngayChieu : date
    giaVe : float
    tblPhim108id : int <<FK>>
    tblPhongChieu108id : int <<FK>>
}

entity "tblHoaDon108" as tblHoaDon {
    * id : int <<PK>>
    --
    maHD : varchar(255)
    ngayTao : date
    tongTien : float
    giamGia : float
    trangThai : int
    tblKhachHang108id : int <<FK>>
}

entity "tblVe108" as tblVe {
    * id : int <<PK>>
    --
    maVe : varchar(255)
    giaBan : float
    tblSuatChieu108id : int <<FK>>
    tblGhe108id : int <<FK>>
    tblHoaDon108id : int <<FK>>
}

tblThanhVien ||--|| tblHoTen
tblKhachHang ||--|| tblThanhVien
tblKhachHang ||--o| tblTheThanhVien
tblPhongChieu ||--|{ tblGhe
tblPhim ||--o{ tblSuatChieu
tblPhongChieu ||--o{ tblSuatChieu
tblSuatChieu ||--|{ tblVe
tblGhe ||--|{ tblVe
tblHoaDon ||--|{ tblVe
tblKhachHang ||--o{ tblHoaDon
@enduml
"""

# 9. Design Class Diagram Module Ban ve (Trang 29 tren PDF)
design_class_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam classAttributeIconSize 0

package "view (JSP)" {
    class GDChinhNVBH108_jsp {
        -subBanVe
    }
    class GDChonPhim108_jsp {
        -inoutChonPhim
        -subTiepTuc
    }
    class GDChonSuatChieu108_jsp {
        -outTenPhim
        -inoutChonSuatChieu
        -subTiepTuc
    }
    class GDChonGhe108_jsp {
        -inoutDanhSachGhe
        -subTiepTuc
    }
    class GDThanhToan108_jsp {
        -outThongTinVe
        -inPhuongThucThanhToan
        -inNhapMathethanhvien
        -subThanhToan
    }
}

package "dao" {
    class DAO {
        -con: Connection
        +DAO()
    }
    class Phim108DAO {
        +getPhim(): List<Phim108>
    }
    class SuatChieu108DAO {
        +getSuatChieuByPhim(idPhim: int): List<Suatchieu108>
    }
    class PhongChieu108DAO {
        +getPhongChieuBySuatChieu(idSC: int): Phongchieu108
    }
    class Ghe108DAO {
        +getGheByPhongChieu(idPC: int): List<Ghe108>
    }
    class HoaDon108DAO {
        +luuHoaDon(hd: Hoadon108): int
    }
    class Ve108DAO {
        +luuVe(ve: Ve108): boolean
    }
    class TheThanhVien108DAO {
        +timThe(maThe: String): Thethanhvien108
    }
}

package "model" {
    class Phim108
    class Suatchieu108
    class Phongchieu108
    class Ghe108
    class Hoadon108
    class Ve108
    class Thethanhvien108
}

Phim108DAO --|> DAO
SuatChieu108DAO --|> DAO
PhongChieu108DAO --|> DAO
Ghe108DAO --|> DAO
HoaDon108DAO --|> DAO
Ve108DAO --|> DAO
TheThanhVien108DAO --|> DAO

GDChonPhim108_jsp ..> Phim108DAO
GDChonSuatChieu108_jsp ..> SuatChieu108DAO
GDChonGhe108_jsp ..> PhongChieu108DAO
GDChonGhe108_jsp ..> Ghe108DAO
GDThanhToan108_jsp ..> HoaDon108DAO
GDThanhToan108_jsp ..> Ve108DAO
GDThanhToan108_jsp ..> TheThanhVien108DAO

Phim108DAO ..> Phim108
SuatChieu108DAO ..> Suatchieu108
PhongChieu108DAO ..> Phongchieu108
Ghe108DAO ..> Ghe108
HoaDon108DAO ..> Hoadon108
Ve108DAO ..> Ve108
TheThanhVien108DAO ..> Thethanhvien108
@enduml
"""

# 10. Activity Diagram Module Ban ve (Trang 30 tren PDF)
activity_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false

|#EBF5FB|GDChinhNVBH108.jsp|
|#E8F8F5|GDChonPhim108.jsp|
|#FEF9E7|GDChonSuatChieu108.jsp|
|#F4ECF7|GDChonGhe108.jsp|
|#FDEDEC|GDThanhToan108.jsp|
|#F2F4F4|DAO & CSDL|

|GDChinhNVBH108.jsp|
start
:Nhận thông tin bán vé;
:click Bán vé;

|GDChonPhim108.jsp|
:Lấy danh sách phim;
|DAO & CSDL|
:Phim108DAO.getPhim();
|GDChonPhim108.jsp|
:Hiển thị danh sách phim;
:Lưu phim đã chọn vào session;
:click tiếp tục;

|GDChonSuatChieu108.jsp|
:Lấy thông tin từ session;
:Lấy danh sách suất chiếu;
|DAO & CSDL|
:SuatChieu108DAO.getSuatChieuByPhim();
|GDChonSuatChieu108.jsp|
:Hiển thị danh sách suất chiếu;
:click chọn tiếp tục;

|GDChonGhe108.jsp|
:Lấy thông tin suất chiếu từ session;
:Lấy danh sách ghế;
|DAO & CSDL|
:Ghe108DAO.getGheByPhongChieu();
|GDChonGhe108.jsp|
:Hiển thị sơ đồ ghế;
:Chọn ghế, đưa vào session;
:click tiếp tục;

|GDThanhToan108.jsp|
:Hiển thị thông tin vé;
:Nhập mã thẻ thành viên (nếu có);
:click thanh toán;
|DAO & CSDL|
:HoaDon108DAO.luuHoaDon();
:Ve108DAO.luuVe();
|GDThanhToan108.jsp|
:Hiển thị thông báo thành công và in vé;
stop
@enduml
"""

# 11. Sequence Design Ban ve (Trang 33 PDF)
seq_design_banve = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam sequenceMessageAlign center

actor "Khách/NV" as Actor
boundary "GDChinh.jsp" as GD0
boundary "GDChonPhim.jsp" as GD1
participant "Phim108DAO" as PDAO
boundary "GDChonSuatChieu.jsp" as GD2
participant "SuatChieu108DAO" as SCDAO
boundary "GDChonGhe.jsp" as GD3
participant "PhongChieu108DAO" as PCDAO
participant "Ghe108DAO" as GDAO
boundary "GDThanhToan.jsp" as GD4
participant "HoaDon108DAO" as HDDAO
participant "Ve108DAO" as VDAO
entity "Phim108" as E1
entity "SuatChieu108" as E2
entity "PhongChieu108" as E3
entity "Ghe108" as E4

Actor -> GD0 : 1: chọn mua vé
activate GD0
GD0 -> GD1 : 2: call
activate GD1
GD1 -> PDAO : 3: call getAllPhim()
activate PDAO
PDAO -> E1 : 4: gọi Phim108
activate E1
E1 --> PDAO : 5: return
deactivate E1
PDAO --> GD1 : 6: return List<Phim108>
deactivate PDAO
GD1 --> Actor : 7: hiển thị
Actor -> GD1 : 8: chọn phim + click tiếp tục

GD1 -> GD2 : 9: call
activate GD2
GD2 -> SCDAO : 10: call getSuatChieuByPhim()
activate SCDAO
SCDAO -> E2 : 11: gọi SuatChieu108
activate E2
E2 --> SCDAO : 12: return
deactivate E2
SCDAO --> GD2 : 13: return List<SuatChieu108>
deactivate SCDAO
GD2 --> Actor : 14: hiển thị
Actor -> GD2 : 15: chọn suất + click tiếp tục

GD2 -> GD3 : 16: call
activate GD3
GD3 -> PCDAO : 17: call getPhongChieuBySuatChieu()
activate PCDAO
PCDAO -> E3 : 18: gọi PhongChieu108
activate E3
E3 --> PCDAO : 19: return
deactivate E3
PCDAO --> GD3 : 20: return PhongChieu108
deactivate PCDAO

GD3 -> GDAO : 21: call getGheByPhongChieu()
activate GDAO
GDAO -> E4 : 22: gọi Ghe108
activate E4
E4 --> GDAO : 23: return
deactivate E4
GDAO --> GD3 : 24: return List<Ghe108>
deactivate GDAO
GD3 --> Actor : 25: hiển thị
Actor -> GD3 : 26: chọn ghế + click tiếp tục

GD3 -> GD4 : 27: call
activate GD4
GD4 --> Actor : 28: hiển thị hóa đơn
Actor -> GD4 : 29: click thanh toán
GD4 -> HDDAO : 30: call luuHoaDon()
activate HDDAO
HDDAO --> GD4 : 31: return idHoaDon
deactivate HDDAO
GD4 -> VDAO : 32: call luuVe()
activate VDAO
VDAO --> GD4 : 33: return success
deactivate VDAO
GD4 --> Actor : 34: hiển thị mua thành công
deactivate GD4
deactivate GD3
deactivate GD2
deactivate GD1
deactivate GD0
@enduml
"""

# 12. Package Diagram (Trang 34 tren PDF)
pkg_diagram = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam packageStyle rectangle

package "webapp" {
    package "modul_1" {
    }
    package "modul_2" {
    }
}

package "dao" {
}

package "entity" {
}

package "util" {
}

webapp ..> dao : <<import>>
modul_1 ..> dao : <<import>>
modul_2 ..> dao : <<import>>

dao ..> entity : <<import>>
dao ..> util : <<import>>
@enduml
"""

# 13. Deployment Diagram (Trang 34 duoi PDF)
deploy_diagram = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false

node "<<device>>\\nClient" as Client #EBF5FB {
    artifact "Web browser\\nHTML\\nJavaScript"
}

node "Application Server" as AppServer #E8F8F5 {
    artifact "Web server\\nHTTP\\nPython / Java"
}

database "Database Server" as DBServer #FEF9E7 {
    artifact "DBMS\\nSQLite / MySQL"
}

Client -- AppServer : HTTP
AppServer -- DBServer : SQL Connection
@enduml
"""

# 14. Module Dang Ky: Analysis Class
analysis_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam classAttributeIconSize 0

class GDChinh108 <<boundary>> {
    -subDangKyThanhVien: submit
}

class GDDangKy108 <<boundary>> {
    -inHoTen: input
    -inSDT: input
    -inEmail: input
    -inCCCD: input
    -inMatKhau: input
    -subLuu: submit
}

class GDKetQuaDangKy108 <<boundary>> {
    -textThongBao: output
    -subQuayLai: submit
}

class Khachhang108 <<entity>> {
    -maKH: String
    -cccd: String
    -diachi: String
    +themKhachHangMoi()
}

class Thethanhvien108 <<entity>> {
    -maThe: String
    -diem: int
    +taoTheThanhVien()
}

GDChinh108 ..> GDDangKy108
GDDangKy108 ..> GDKetQuaDangKy108
GDDangKy108 ..> Khachhang108 : themKhachHangMoi()
GDDangKy108 ..> Thethanhvien108 : taoTheThanhVien()
Khachhang108 "1" *-- "1" Thethanhvien108
@enduml
"""

# 15. Module Dang Ky: Communication Diagram
comm_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false

actor "Khách hàng" as KH
boundary "GDChinh108" as GDChinh
boundary "GDDangKy108" as GDDangKy
boundary "GDKetQuaDangKy108" as GDKetQua
entity "Khachhang108" as EKH
entity "Thethanhvien108" as EThe

KH -> GDChinh : 1: Chọn đăng ký
GDChinh -> GDDangKy : 2: Gọi
GDDangKy -> KH : 3: Hiển thị form
KH -> GDDangKy : 4: Nhập thông tin + Click đăng ký
GDDangKy -> EKH : 5: Gọi themKhachHangMoi()
EKH -> EThe : 6: taoTheThanhVien()
EThe -> EKH : 7: Trả về
EKH -> GDDangKy : 8: Trả về kết quả
GDDangKy -> GDKetQua : 9: Gọi
GDKetQua -> KH : 10: Thông báo thành công & Mã thẻ
@enduml
"""

# 16. Module Dang Ky: Sequence Analysis Diagram
seq_analysis_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam sequenceMessageAlign center

actor "Khách hàng" as KH
boundary "GDChinh108" as GD0
boundary "GDDangKy108" as GD1
boundary "GDKetQuaDangKy108" as GD2
entity "Khachhang108" as EKH
entity "Thethanhvien108" as EThe

KH -> GD0 : 1: Chọn đăng ký
activate GD0
GD0 -> GD1 : 2: Gọi
activate GD1
GD1 --> KH : 3: Hiển thị form
KH -> GD1 : 4: Nhập thông tin + click đăng ký
GD1 -> EKH : 5: themKhachHangMoi()
activate EKH
EKH -> EThe : 6: taoTheThanhVien()
activate EThe
EThe --> EKH : 7: return theThanhVien
deactivate EThe
EKH --> GD1 : 8: return ketQua
deactivate EKH
GD1 -> GD2 : 9: Gọi
activate GD2
GD2 --> KH : 10: Thông báo thành công & Mã thẻ
deactivate GD2
deactivate GD1
deactivate GD0
@enduml
"""

# 17. Module Dang Ky: Design Class Diagram
design_class_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam classAttributeIconSize 0

package "view (JSP)" {
    class GDChinh108_jsp {
        -subDangKy
    }
    class GDDangKy108_jsp {
        -inHoTen
        -inSDT
        -inEmail
        -inCCCD
        -inMatKhau
        -subLuu
    }
    class GDKetQuaDangKy108_jsp {
        -outThongBao
        -subQuayLai
    }
}

package "dao" {
    class DAO {
        -con: Connection
    }
    class KhachHang108DAO {
        +themKhachHang(kh: Khachhang108): boolean
        +kiemTraTrung(sdt: String, email: String): boolean
    }
    class TheThanhVien108DAO {
        +themThe(the: Thethanhvien108): boolean
    }
}

package "model" {
    class Khachhang108
    class Thethanhvien108
}

KhachHang108DAO --|> DAO
TheThanhVien108DAO --|> DAO
GDDangKy108_jsp ..> KhachHang108DAO
GDDangKy108_jsp ..> TheThanhVien108DAO
KhachHang108DAO ..> Khachhang108
TheThanhVien108DAO ..> Thethanhvien108
@enduml
"""

# 18. Module Dang Ky: Activity Diagram
activity_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false

|#EBF5FB|GDDangKy108.jsp|
|#FEF9E7|KhachHang108DAO|
|#F2F4F4|CSDL SQLite|

|GDDangKy108.jsp|
start
:Hiển thị form điền thông tin cá nhân;
:Nhập họ tên, SĐT, email, CCCD, mật khẩu;
:click Đăng ký;
|KhachHang108DAO|
:Đưa thông tin vào DAO;
:Kiểm tra trùng lặp dữ liệu;
if (Dữ liệu hợp lệ & Không trùng?) then (Có)
    |CSDL SQLite|
    :Lưu vào tblKhachHang108;
    :Tự sinh mã thẻ, lưu vào tblTheThanhVien108;
    |GDDangKy108.jsp|
    :GDKetQuaDangKy108.jsp hiển thị thông báo thành công và mã thẻ;
    stop
else (Không)
    |GDDangKy108.jsp|
    :Hiển thị thông báo lỗi nhập liệu;
    stop
endif
@enduml
"""

# 19. Module Dang Ky: Sequence Design Diagram
seq_design_dangky = """@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam sequenceMessageAlign center

actor "Khách hàng" as KH
boundary "GDDangKy108.jsp" as View
participant "KhachHang108DAO" as KHDAO
participant "TheThanhVien108DAO" as TheDAO
boundary "GDKetQuaDangKy108.jsp" as Result
database "CSDL SQLite" as DB

KH -> View : 1: nhập thông tin + click Lưu
activate View
View -> KHDAO : 2: call kiemTraTrung()
activate KHDAO
KHDAO -> DB : 3: executeQuery()
activate DB
DB --> KHDAO : 4: return kết quả
deactivate DB
KHDAO --> View : 5: hợp lệ
deactivate KHDAO

View -> KHDAO : 6: call themKhachHang(kh)
activate KHDAO
KHDAO -> DB : 7: executeUpdate()
activate DB
DB --> KHDAO : 8: idKhachHangMoi
deactivate DB
KHDAO --> View : 9: return true
deactivate KHDAO

View -> TheDAO : 10: call themThe(the)
activate TheDAO
TheDAO -> DB : 11: executeUpdate()
activate DB
DB --> TheDAO : 12: return 1
deactivate DB
TheDAO --> View : 13: return true
deactivate TheDAO

View -> Result : 14: chuyển tiếp kết quả
activate Result
Result --> KH : 15: hiển thị đăng ký thành công & mã thẻ
deactivate Result
deactivate View
@enduml
"""

diagrams = {
    "01_usecase_tongquan_108.puml": uc_tongquan,
    "02_usecase_chitiet_dangky_108.puml": uc_dangky,
    "03_usecase_chitiet_banve_108.puml": uc_banve,
    "04_entity_class_diagram_108.puml": entity_diagram,
    "05_analysis_class_banve_108.puml": analysis_banve,
    "06_communication_banve_108.puml": comm_banve,
    "07_sequence_analysis_banve_108.puml": seq_analysis_banve,
    "08_database_schema_108.puml": db_schema,
    "09_design_class_banve_108.puml": design_class_banve,
    "10_activity_banve_108.puml": activity_banve,
    "11_sequence_design_banve_108.puml": seq_design_banve,
    "12_package_diagram_108.puml": pkg_diagram,
    "13_deployment_diagram_108.puml": deploy_diagram,
    "14_analysis_class_dangky_108.puml": analysis_dangky,
    "15_communication_dangky_108.puml": comm_dangky,
    "16_sequence_analysis_dangky_108.puml": seq_analysis_dangky,
    "17_design_class_dangky_108.puml": design_class_dangky,
    "18_activity_dangky_108.puml": activity_dangky,
    "19_sequence_design_dangky_108.puml": seq_design_dangky
}

for name, content in diagrams.items():
    file_path = os.path.join(uml_dir, name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {name}")
