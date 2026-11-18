# CineMan - Hệ Thống Quản Lý Rạp Chiếu Phim

> **Đồ án môn học:** Phân tích & Thiết kế Hệ thống Thông tin (PTTKHTTT)  
> **Khoa:** Công nghệ Thông tin 1 - Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
> **Giảng viên hướng dẫn:** ThS. Đặng Thị Bích Ngọc (Email: `dtbnptit@gmail.com`)  

---

## 1. Giới thiệu dự án
Hệ thống **CineMan** là phần mềm quản lý rạp chiếu phim hiện đại theo kiến trúc phân tầng (Tiered / MVC), hỗ trợ 3 nhóm tác nhân chính:
1. **Nhân viên Quản lý (Manager):** Xem các báo cáo thống kê chuyên sâu (doanh thu theo ngày/tháng, top phim ăn khách, khách hàng thân thiết); Quản lý thông tin phim (Thêm/Sửa/Xóa); Quản lý phòng chiếu và sơ đồ ghế; Lên lịch suất chiếu.
2. **Nhân viên Bán hàng (Cashier / POS):** Bán vé xem phim trực tiếp tại quầy theo quy trình chuẩn: Tìm kiếm phim -> Chọn suất chiếu -> Chọn ghế ngồi trên sơ đồ trực quan -> Quét/Nhập thẻ thành viên (tự động chiết khấu 5% - 15% & tích điểm) -> Thanh toán -> In vé và hóa đơn. Xuất/cấp thẻ thành viên mới cho khách.
3. **Khách hàng (Customer):** Đăng ký tài khoản thành viên trực tuyến nhận thẻ điện tử và điểm thưởng; Tra cứu thông tin phim và lịch chiếu.

---

## 2. Cấu trúc thư mục (Kiến trúc chuẩn MVC)
```text
cineman/
├── app.py                      # Flask Application Web Server & Routing
├── controllers/                # Business Logic Layer (Các lớp điều khiển nghiệp vụ)
│   ├── auth_controller.py      # Xác thực đăng nhập & phiên làm việc
│   ├── ban_ve_controller.py    # Xử lý quy trình bán vé POS, tính tiền & tích điểm
│   ├── khach_hang_controller.py# Quản lý khách hàng & đăng ký thành viên
│   ├── phim_controller.py      # Nghiệp vụ quản lý phim & lịch chiếu
│   └── thong_ke_controller.py  # Xử lý tổng hợp số liệu báo cáo
├── dao/                        # Data Access Layer (Truy xuất CSDL SQLite)
│   ├── db_connection.py        # Quản lý kết nối CSDL (Singleton Pattern)
│   ├── khach_hang_dao.py       # Thao tác bảng tblKhachHang & tblTheThanhVien
│   ├── phim_dao.py             # Thao tác bảng tblPhim
│   ├── phong_chieu_dao.py      # Thao tác bảng tblPhongChieu
│   ├── lich_chieu_dao.py       # Thao tác bảng tblLichChieu
│   ├── ghe_dao.py              # Thao tác bảng tblGhe & kiểm tra trạng thái ghế
│   ├── hoa_don_dao.py          # Thao tác bảng tblHoaDon
│   ├── ve_dao.py               # Thao tác bảng tblVe
│   └── thong_ke_dao.py         # Thao tác truy vấn thống kê KPI
├── database/                   # Cơ sở dữ liệu SQLite & script khởi tạo
│   ├── cineman.db              # File cơ sở dữ liệu quan hệ
│   └── init_db.py              # Script tạo bảng và chèn dữ liệu mẫu thực tế
├── models/                     # Domain Model Entities (Các lớp thực thể nghiệp vụ)
│   ├── __init__.py
│   └── entities.py             # NguoiDung, NhanVien, KhachHang, TheThanhVien, Phim, PhongChieu, Ghe, LichChieu, Ve, HoaDon
├── templates/                  # Presentation Layer (Giao diện HTML5 / Jinja2 / Bootstrap 5)
│   ├── base.html               # Layout khung rạp phim cinema hiện đại
│   ├── login.html              # Màn hình đăng nhập (có nút autofill tài khoản demo)
│   ├── register.html           # Màn hình đăng ký thành viên
│   ├── register_success.html   # Thông báo thành công & thẻ thành viên điện tử
│   ├── staff_pos.html          # Màn hình POS Bán vé tại quầy trực quan
│   ├── ticket_print.html       # Mẫu in Vé xem phim và Hóa đơn thanh toán
│   ├── manager_dashboard.html  # Dashboard thống kê doanh thu, phim, khách hàng
│   ├── manager_movies.html     # Quản lý phim (CRUD)
│   ├── manager_schedules.html  # Lên lịch chiếu
│   ├── manager_customers.html  # Danh sách khách hàng & thẻ
│   └── customer_home.html      # Trang chủ khách hàng
├── static/                     # Tệp tĩnh CSS, JavaScript, ảnh
└── README.md                   # Tài liệu hướng dẫn cài đặt và sử dụng
```

---

## 3. Hướng dẫn cài đặt và chạy ứng dụng

### Bước 1: Cài đặt thư viện yêu cầu
Dự án sử dụng Python 3.8+ và thư viện Flask:
```bash
pip install flask
```

### Bước 2: Khởi tạo Cơ sở dữ liệu (Database)
Nếu muốn reset hoặc khởi tạo CSDL với dữ liệu mẫu:
```bash
python database/init_db.py
```

### Bước 3: Khởi chạy máy chủ Web
```bash
python app.py
```
Sau khi chạy, truy cập trình duyệt tại địa chỉ: **`http://127.0.0.1:5000`**

---

## 4. Danh sách tài khoản thử nghiệm (Demo Accounts)

| Vai trò | Tên đăng nhập | Mật khẩu | Chức năng chính |
| :--- | :--- | :--- | :--- |
| **Quản lý rạp** | `admin` | `admin123` | Xem báo cáo thống kê, Quản lý phim, Lên lịch chiếu |
| **Nhân viên bán hàng** | `staff` | `staff123` | Bán vé tại quầy (POS), Chọn ghế, Áp dụng thẻ, In hóa đơn |
| **Khách hàng thân thiết (VIP)** | `customer` | `customer123` | Mã thẻ: `MB-8888`, giảm giá 15% |
| **Khách hàng thân thiết (Gold)**| `hoangnam` | `pass123` | Mã thẻ: `MB-9999`, giảm giá 10% |

*(Tại màn hình Đăng nhập, hệ thống có sẵn các nút bấm 1-click để tự động điền tài khoản nhanh chóng).*

---

## 5. Hướng dẫn nộp bài cho Giảng viên trên GitHub
Để chia sẻ quyền cho giảng viên chấm bài theo đúng yêu cầu:
1. Tạo một repository mới trên GitHub cá nhân (đặt tên: `CineMan-CinemaManagement`).
2. Mở terminal tại thư mục dự án và thực thi:
   ```bash
   git init
   git add .
   git commit -m "CineMan: Hệ thống quản lý rạp chiếu phim PTIT"
   git branch -M main
   git remote add origin https://github.com/<username-cua-ban>/CineMan-CinemaManagement.git
   git push -u origin main
   ```
3. Truy cập GitHub Repo -> **Settings** -> **Collaborators** -> Nhấn **Add people** -> Nhập email: `dtbnptit@gmail.com` -> Gửi lời mời.
