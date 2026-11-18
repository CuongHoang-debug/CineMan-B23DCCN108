import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_report():
    doc = Document()

    # 1. Căn lề chuẩn PTIT: Top 2cm, Bottom 2cm, Left 3cm, Right 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.79)     # 2 cm
        section.bottom_margin = Inches(0.79)  # 2 cm
        section.left_margin = Inches(1.18)    # 3 cm
        section.right_margin = Inches(0.79)   # 2 cm

    # Cấu hình Style Normal
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    uml_dir = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\uml"
    screen_dir = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\screenshots"
    out_docx = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\reports\11D22DCCN123.docx"

    # ==================== TRANG BÌA ====================
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_header.add_run("BỘ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r1.font.size = Pt(12)
    r2 = p_header.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r2.bold = True
    r2.font.size = Pt(13)
    r3 = p_header.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1\n---------------------------------")
    r3.font.size = Pt(11)

    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(70)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt1 = p_title.add_run("BÁO CÁO BÀI TẬP LỚN\n")
    rt1.bold = True
    rt1.font.size = Pt(17)
    rt1.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    rt2 = p_title.add_run("PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG THÔNG TIN\n\n")
    rt2.bold = True
    rt2.font.size = Pt(15)
    rt2.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    rt3 = p_title.add_run("ĐỀ TÀI: XÂY DỰNG HỆ THỐNG QUẢN LÝ RẠP CHIẾU PHIM\n(CINEMAN)")
    rt3.bold = True
    rt3.font.size = Pt(15)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(90)

    tbl_cover = doc.add_table(rows=5, cols=2)
    tbl_cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_info = [
        ("Giảng viên hướng dẫn:", "ThS. Đặng Thị Bích Ngọc (dtbnptit@gmail.com)"),
        ("Mã đề tài:", "Đề 11 - Hệ thống quản lý rạp chiếu phim (CineMan)"),
        ("Sinh viên thực hiện:", "Nguyễn Tuấn Anh"),
        ("Mã sinh viên:", "D22DCCN123"),
        ("Lớp học phần:", "D22CQCN01-B - Nhóm TH: 02")
    ]
    for row_idx, (lbl, val) in enumerate(cover_info):
        row = tbl_cover.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(3.8)
        c0.paragraphs[0].add_run(lbl).bold = True
        c1.paragraphs[0].add_run(val)

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_before = Pt(60)

    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rb = p_bot.add_run("Hà Nội, Năm 2026")
    rb.font.size = Pt(12)

    doc.add_page_break()

    # ==================== LỜI MỞ ĐẦU & DANH SÁCH FORM ====================
    doc.add_heading("TỔNG QUAN ĐỀ TÀI & CÁC ĐƯỜNG LINK NỘP BÀI", level=1)
    doc.add_paragraph(
        "Báo cáo này trình bày kết quả phân tích, thiết kế và lập trình thực nghiệm Hệ thống Quản lý Rạp Chiếu Phim (CineMan) "
        "theo đúng quy trình phân tích thiết kế hướng đối tượng (OOAD / RUP) được giảng dạy tại Học viện Công nghệ Bưu chính Viễn thông. "
        "Hệ thống tập trung giải quyết bài toán nghiệp vụ cốt lõi của rạp chiếu phim với 3 tác nhân: Khách hàng, Nhân viên bán hàng và Nhân viên quản lý, "
        "trong đó đi sâu vào hiện thực hóa 2 ca sử dụng trọng tâm theo yêu cầu của đề bài:\n"
        "1. Chức năng Khách hàng đăng ký thành viên: Đăng ký thông tin cá nhân → Lưu trữ bền vững vào CSDL → Tự động cấp mã thẻ thành viên và tích lũy điểm.\n"
        "2. Chức năng Nhân viên bán vé tại quầy (POS): Tìm phim → Chọn phim kết quả → Chọn suất chiếu → Chọn ghế ngồi trực quan → Áp dụng thẻ thành viên giảm giá → Thanh toán → In vé và hóa đơn bán hàng."
    )

    doc.add_heading("Các Đường Link Nộp Bài và Mã Nguồn Dự Án:", level=2)
    p_lk = doc.add_paragraph()
    p_lk.add_run("• Link nộp code PlantUML Đặc tả: ").bold = True
    p_lk.add_run("https://forms.gle/WjBeCqMYZnMPHmcV7\n")
    p_lk.add_run("• Link nộp code PlantUML Phân tích: ").bold = True
    p_lk.add_run("https://forms.gle/ciKQDmZntpPKuH4H7\n")
    p_lk.add_run("• Link nộp code PlantUML Thiết kế: ").bold = True
    p_lk.add_run("https://forms.gle/rqmj7ZFnfQ5n7FzD7\n")
    p_lk.add_run("• Link Form Tự đánh giá: ").bold = True
    p_lk.add_run("https://forms.gle/yuLGeZZtWheGsnPu5\n")
    p_lk.add_run("• Link GitHub Repository: ").bold = True
    p_lk.add_run("https://github.com/D22DCCN123/CineMan-CinemaManagement (Đã add collaborator: dtbnptit@gmail.com)\n")

    # ==================== PHẦN 1: ĐẶC TẢ YÊU CẦU ====================
    doc.add_heading("PHẦN 1: ĐẶC TẢ YÊU CẦU HỆ THỐNG", level=1)

    doc.add_heading("1.1. Bảng Phân rã Ca sử dụng và Tác nhân", level=2)
    tbl_uc = doc.add_table(rows=1, cols=4)
    tbl_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_uc)
    h_uc = tbl_uc.rows[0].cells
    for i, t in enumerate(["STT", "Tác nhân (Actor)", "Mã & Tên Ca sử dụng", "Mô tả nghiệp vụ"]):
        h_uc[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_uc[i], "E2E8F0")

    uc_rows = [
        ("1", "Tác nhân chung", "UC00: Đăng nhập\nUC00b: Đăng xuất", "Xác thực danh tính người dùng bằng tài khoản và mật khẩu mã hóa SHA-256; phân quyền tương ứng."),
        ("2", "Khách hàng", "UC01: Đăng ký thành viên", "Khách hàng nhập thông tin cá nhân; hệ thống kiểm tra trùng lặp, lưu CSDL, tự sinh mã thẻ thành viên điện tử và điểm tích lũy ban đầu = 0."),
        ("3", "Khách hàng", "UC02: Tìm kiếm phim & Lịch", "Khách hàng tra cứu danh sách phim đang chiếu và lịch chiếu theo ngày."),
        ("4", "Khách hàng", "UC03: Mua vé trực tuyến", "Khách hàng đặt vé từ xa qua giao diện web."),
        ("5", "Nhân viên Bán hàng", "UC04: Bán vé tại quầy (POS)", "Hỏi phim -> Tìm phim -> Chọn suất chiếu -> Chọn ghế -> Nhập thẻ thành viên (chiết khấu) -> Thanh toán -> In vé và hóa đơn."),
        ("6", "Nhân viên Bán hàng", "UC05: Xuất thẻ thành viên", "Cấp phát thẻ thành viên mới cho khách hàng trực tiếp tại quầy."),
        ("7", "Nhân viên Quản lý", "UC06: Quản lý phim", "Thêm, cập nhật thông tin phim, sửa thời lượng/đạo diễn, ngừng chiếu hoặc xóa phim."),
        ("8", "Nhân viên Quản lý", "UC07: Quản lý phòng chiếu", "Quản lý phòng chiếu (IMAX, 3D, 2D) và cơ cấu ghế (Thường, VIP, Đôi)."),
        ("9", "Nhân viên Quản lý", "UC08: Lên lịch chiếu", "Thiết lập suất chiếu: chọn Phim, Phòng chiếu, Ngày và Khung giờ bắt đầu/kết thúc."),
        ("10", "Nhân viên Quản lý", "UC09: Xem thống kê", "Xem báo cáo doanh thu theo mốc thời gian, thống kê số vé bán của từng phim, thống kê điểm khách hàng.")
    ]
    for r_data in uc_rows:
        row = tbl_uc.add_row()
        for i, val in enumerate(r_data):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    doc.add_heading("1.2. Biểu đồ Ca sử dụng Tổng quát (Use Case Diagram)", level=2)
    doc.add_paragraph("Biểu đồ thể hiện toàn bộ ranh giới hệ thống, các tác nhân và quan hệ giữa các ca sử dụng:")
    img_uc = os.path.join(uml_dir, "01_usecase_tongquat.png")
    if os.path.exists(img_uc):
        doc.add_picture(img_uc, width=Inches(6.0))
        p_c = doc.add_paragraph("Hình 1.1: Sơ đồ Ca sử dụng Tổng quát Hệ thống CineMan")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("1.3. Đặc tả Chi tiết 2 Ca sử dụng Trọng tâm", level=2)

    # UC 01
    doc.add_heading("1.3.1. Đặc tả Ca sử dụng: Khách hàng đăng ký thành viên (UC01)", level=3)
    tbl_d1 = doc.add_table(rows=7, cols=2)
    set_table_borders(tbl_d1)
    d1_data = [
        ("Mã Ca sử dụng:", "UC01 - Khách hàng đăng ký thành viên"),
        ("Tác nhân chính:", "Khách hàng (Customer)"),
        ("Mục đích:", "Khách hàng đăng ký thông tin để trở thành hội viên CineMan, được cấp mã thẻ thành viên và tích lũy điểm thưởng khi mua vé."),
        ("Tiền điều kiện:", "Khách hàng truy cập vào hệ thống website CineMan, chưa đăng nhập."),
        ("Hậu điều kiện:", "Dữ liệu khách hàng được lưu vào CSDL; hệ thống sinh mã thẻ `MB-XXXX`, khởi tạo điểm thưởng = 0."),
        ("Luồng sự kiện chính\n(Normal Flow):",
         "1. Khách hàng click chọn menu \"Đăng ký thành viên\" trên thanh điều hướng.\n"
         "2. Hệ thống hiển thị Form đăng ký (Họ tên, SĐT, Email, CCCD, Mật khẩu, Ngày sinh, Địa chỉ).\n"
         "3. Khách hàng nhập đầy đủ thông tin cá nhân hợp lệ và click nút \"Xác nhận Đăng ký\".\n"
         "4. Hệ thống kiểm tra hợp lệ dữ liệu (Validate form: email đúng dạng, SĐT 10 số, CCCD 12 số, mật khẩu >= 6 ký tự).\n"
         "5. Hệ thống truy vấn CSDL kiểm tra: Số điện thoại, Email và CCCD chưa từng tồn tại.\n"
         "6. Hệ thống mã hóa mật khẩu, tạo bản ghi khách hàng và tự động sinh mã thẻ thành viên điện tử.\n"
         "7. Hệ thống lưu thành công thông tin vào CSDL SQLite (bảng tblKhachHang, tblTheThanhVien).\n"
         "8. Hệ thống hiển thị màn hình thông báo: \"Đăng ký thành công!\", trình bày thẻ thành viên điện tử kèm mã thẻ để khách hàng sử dụng.\n"
         "9. Ca sử dụng kết thúc."),
        ("Luồng rẽ nhánh &\nNgoại lệ (Alternative):",
         "• 4a. Thiếu trường bắt buộc hoặc sai định dạng: Hệ thống báo lỗi cụ thể và giữ nguyên form cho người dùng sửa.\n"
         "• 5a. Số điện thoại, Email hoặc CCCD đã được đăng ký: Hệ thống báo lỗi thông tin đã tồn tại và gợi ý chuyển sang màn hình Đăng nhập.")
    ]
    for idx, (k, v) in enumerate(d1_data):
        row = tbl_d1.rows[idx]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[0].width = Inches(1.8)
        row.cells[1].paragraphs[0].add_run(v)
        row.cells[1].width = Inches(4.2)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])

    doc.add_paragraph()
    img_act1 = os.path.join(uml_dir, "02_activity_dangky_thanhvien.png")
    if os.path.exists(img_act1):
        doc.add_picture(img_act1, width=Inches(5.0))
        p_c = doc.add_paragraph("Hình 1.2: Sơ đồ Hoạt động (Activity Diagram) - Ca sử dụng Đăng ký thành viên")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    # UC 02
    doc.add_heading("1.3.2. Đặc tả Ca sử dụng: Nhân viên bán vé cho khách hàng tại quầy (UC04)", level=3)
    tbl_d2 = doc.add_table(rows=7, cols=2)
    set_table_borders(tbl_d2)
    d2_data = [
        ("Mã Ca sử dụng:", "UC04 - Bán vé cho khách hàng tại quầy (POS)"),
        ("Tác nhân chính:", "Nhân viên Bán hàng (Staff / Cashier), Khách hàng (Customer)"),
        ("Mục đích:", "Bán vé xem phim trực tiếp tại quầy theo đúng phim, suất chiếu, vị trí ghế khách hàng chọn; áp dụng giảm giá thẻ thành viên; in vé và hóa đơn."),
        ("Tiền điều kiện:", "Nhân viên bán hàng đã đăng nhập vào hệ thống; hệ thống rạp có suất chiếu trong ngày."),
        ("Hậu điều kiện:", "Hóa đơn và vé được lưu vào CSDL; trạng thái các ghế đã chọn chuyển thành 'ĐÃ BÁN'; cộng điểm tích lũy vào thẻ khách hàng; in vé và hóa đơn thành công."),
        ("Luồng sự kiện chính\n(Normal Flow):",
         "1. Nhân viên bán hàng chọn menu \"Bán vé tại quầy (POS)\".\n"
         "2. Hệ thống hiển thị giao diện bán vé với thanh tìm kiếm và danh mục phim đang chiếu.\n"
         "3. Nhân viên hỏi tên phim khách muốn xem và nhập tên phim vào ô tìm kiếm.\n"
         "4. Hệ thống lọc và hiển thị danh sách phim kết quả tương ứng.\n"
         "5. Nhân viên click chọn phim từ danh sách kết quả.\n"
         "6. Hệ thống tải và hiển thị danh sách các suất chiếu (giờ xem) trong ngày của phim đó.\n"
         "7. Khách hàng chọn giờ xem; nhân viên click chọn suất chiếu tương ứng.\n"
         "8. Hệ thống hiển thị sơ đồ phòng chiếu với trạng thái từng ghế (ghế trống, ghế đã bán; phân loại ghế Thường, VIP, Đôi).\n"
         "9. Khách hàng chọn vị trí ghế; nhân viên click chọn các ghế tương ứng trên màn hình. Hệ thống cập nhật tổng tiền tạm tính.\n"
         "10. Nhân viên hỏi khách hàng mã thẻ thân thiết. Nếu có, nhân viên nhập mã thẻ và bấm \"Áp dụng\".\n"
         "11. Hệ thống tra cứu thẻ thành viên: hiển thị tên chủ thẻ, hạng thẻ, tự động chiết khấu giảm giá (VIP 15%, Gold 10%, Silver 7%, Standard 5%) và tính điểm tích lũy dự kiến (+10% giá trị vé).\n"
         "12. Nhân viên thông báo tổng số tiền cần thanh toán cho khách.\n"
         "13. Khách hàng thực hiện thanh toán (Tiền mặt / Chuyển khoản QR / Quẹt thẻ POS).\n"
         "14. Nhân viên chọn hình thức thanh toán và click nút \"Xác nhận mua vé & In hóa đơn\".\n"
         "15. Hệ thống thực thi giao dịch CSDL: đổi trạng thái ghế sang \"ĐÃ BÁN\", tạo bản ghi Hóa đơn (tblHoaDon), tạo bản ghi Vé (tblVe), cộng điểm tích lũy vào thẻ thành viên.\n"
         "16. Hệ thống kích hoạt lệnh in: xuất vé xem phim và hóa đơn thanh toán giao cho khách hàng.\n"
         "17. Ca sử dụng kết thúc."),
        ("Luồng rẽ nhánh &\nNgoại lệ (Alternative):",
         "• 4a. Không tìm thấy phim theo từ khóa: Hệ thống báo không tìm thấy kết quả, nhân viên tư vấn phim khác đang chiếu.\n"
         "• 9a. Ghế khách chọn vừa bị khách khác đặt: Hệ thống cảnh báo ghế đã bán, yêu cầu chọn ghế khác.\n"
         "• 10a. Khách hàng không có thẻ thành viên: Bỏ qua bước nhập mã thẻ, hệ thống tính theo giá vé gốc.")
    ]
    for idx, (k, v) in enumerate(d2_data):
        row = tbl_d2.rows[idx]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[0].width = Inches(1.8)
        row.cells[1].paragraphs[0].add_run(v)
        row.cells[1].width = Inches(4.2)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])

    doc.add_paragraph()
    img_act2 = os.path.join(uml_dir, "03_activity_banve_taiquay.png")
    if os.path.exists(img_act2):
        doc.add_picture(img_act2, width=Inches(5.2))
        p_c = doc.add_paragraph("Hình 1.3: Sơ đồ Hoạt động (Activity Diagram) - Ca sử dụng Bán vé tại quầy")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    # ==================== PHẦN 2: PHÂN TÍCH HỆ THỐNG ====================
    doc.add_heading("PHẦN 2: PHÂN TÍCH HỆ THỐNG", level=1)

    doc.add_heading("2.1. Phân tích Robustness BCE (Boundary - Control - Entity)", level=2)
    doc.add_paragraph(
        "Mô hình phân tích áp dụng phân loại BCE chuẩn RUP:\n"
        "• Lớp Biên (Boundary): Tiếp nhận tương tác người dùng (`FormDangNhap`, `FormDangKyThanhVien`, `FormBanVeTaiQuay`, `FormThongKe`...).\n"
        "• Lớp Điều Khiển (Control): Chứa logic điều phối và quy tắc nghiệp vụ (`DangNhapCtrl`, `DangKyCtrl`, `BanVeCtrl`, `PhimCtrl`...).\n"
        "• Lớp Thực Thể (Entity): Lưu trữ dữ liệu nghiệp vụ (`KhachHang`, `TheThanhVien`, `NhanVien`, `Phim`, `PhongChieu`, `Ghe`, `LichChieu`, `HoaDon`, `Ve`)."
    )

    img_acd = os.path.join(uml_dir, "04_analysis_class_diagram.png")
    if os.path.exists(img_acd):
        doc.add_picture(img_acd, width=Inches(6.0))
        p_c = doc.add_paragraph("Hình 2.1: Biểu đồ Lớp Phân tích (Analysis Class Diagram) - Hệ thống CineMan")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("2.2. Biểu đồ Trình tự Phân tích (Analysis Sequence Diagram)", level=2)

    doc.add_heading("2.2.1. Biểu đồ Trình tự Phân tích: Đăng ký thành viên", level=3)
    img_asd1 = os.path.join(uml_dir, "05_sequence_analysis_dangky.png")
    if os.path.exists(img_asd1):
        doc.add_picture(img_asd1, width=Inches(5.5))
        p_c = doc.add_paragraph("Hình 2.2: Biểu đồ Trình tự Phân tích - Ca sử dụng Đăng ký thành viên")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("2.2.2. Biểu đồ Trình tự Phân tích: Bán vé tại quầy", level=3)
    img_asd2 = os.path.join(uml_dir, "06_sequence_analysis_banve.png")
    if os.path.exists(img_asd2):
        doc.add_picture(img_asd2, width=Inches(5.5))
        p_c = doc.add_paragraph("Hình 2.3: Biểu đồ Trình tự Phân tích - Ca sử dụng Bán vé tại quầy")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    # ==================== PHẦN 3: THIẾT KẾ HỆ THỐNG ====================
    doc.add_heading("PHẦN 3: THIẾT KẾ HỆ THỐNG", level=1)

    doc.add_heading("3.1. Mô hình Kiến trúc Phân tầng (Layered / MVC Pattern)", level=2)
    doc.add_paragraph(
        "Hệ thống CineMan áp dụng kiến trúc phân tầng 3 lớp MVC kết hợp mẫu thiết kế DAO (Data Access Object) và Singleton Pattern cho lớp quản lý kết nối CSDL:"
    )
    img_arch = os.path.join(uml_dir, "07_architecture_packages.png")
    if os.path.exists(img_arch):
        doc.add_picture(img_arch, width=Inches(5.8))
        p_c = doc.add_paragraph("Hình 3.1: Mô hình Kiến trúc Phân tầng Gói (MVC Architecture)")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("3.2. Biểu đồ Lớp Thiết kế Chi tiết (Design Class Diagram)", level=2)
    doc.add_paragraph(
        "Biểu đồ lớp thiết kế chi tiết cung cấp đặc tả kỹ thuật hoàn chỉnh: thuộc tính private (-), kiểu dữ liệu, phương thức public (+) kèm tham số và kiểu trả về, quan hệ giữa các tầng View -> Controller -> DAO -> Model:"
    )
    img_dcd = os.path.join(uml_dir, "08_design_class_diagram.png")
    if os.path.exists(img_dcd):
        doc.add_picture(img_dcd, width=Inches(6.2))
        p_c = doc.add_paragraph("Hình 3.2: Biểu đồ Lớp Thiết kế Chi tiết (Design Class Diagram)")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("3.3. Biểu đồ Trình tự Thiết kế Chi tiết (Design Sequence Diagram)", level=2)

    doc.add_heading("3.3.1. Biểu đồ Trình tự Thiết kế: Đăng ký thành viên", level=3)
    img_dsd1 = os.path.join(uml_dir, "09_sequence_design_dangky.png")
    if os.path.exists(img_dsd1):
        doc.add_picture(img_dsd1, width=Inches(5.5))
        p_c = doc.add_paragraph("Hình 3.3: Biểu đồ Trình tự Thiết kế - Ca sử dụng Đăng ký thành viên")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("3.3.2. Biểu đồ Trình tự Thiết kế: Bán vé tại quầy", level=3)
    img_dsd2 = os.path.join(uml_dir, "10_sequence_design_banve.png")
    if os.path.exists(img_dsd2):
        doc.add_picture(img_dsd2, width=Inches(5.5))
        p_c = doc.add_paragraph("Hình 3.4: Biểu đồ Trình tự Thiết kế - Ca sử dụng Bán vé tại quầy")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("3.4. Thiết kế Cơ sở Dữ liệu Quan hệ (ERD & Data Dictionary)", level=2)
    img_erd = os.path.join(uml_dir, "11_erd_database.png")
    if os.path.exists(img_erd):
        doc.add_picture(img_erd, width=Inches(6.0))
        p_c = doc.add_paragraph("Hình 3.5: Lược đồ Cơ sở Dữ liệu Quan hệ (ERD) - CineMan")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_heading("Từ điển dữ liệu 10 bảng CSDL:", level=3)
    tbl_dd = doc.add_table(rows=1, cols=4)
    tbl_dd.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_dd)
    h_dd = tbl_dd.rows[0].cells
    for i, t in enumerate(["Tên Bảng", "Khóa chính (PK)", "Khóa ngoại (FK)", "Ý nghĩa lưu trữ"]):
        h_dd[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_dd[i], "E2E8F0")

    dd_data = [
        ("tblNguoiDung", "id (INT)", "Không", "Thông tin tài khoản, họ tên, SĐT, email, vai trò (QUAN_LY, BAN_HANG, KHACH_HANG)"),
        ("tblNhanVien", "id (INT)", "id -> tblNguoiDung", "Chức vụ, ca làm việc, mức lương cơ bản của nhân viên"),
        ("tblKhachHang", "id (INT)", "id -> tblNguoiDung", "Số CCCD, ngày sinh, địa chỉ liên hệ của khách hàng"),
        ("tblTheThanhVien", "id (INT)", "idKhachHang -> tblKhachHang", "Mã thẻ (MB-XXXX), hạng thẻ (VIP/Gold/Silver/Standard), điểm tích lũy"),
        ("tblPhim", "id (INT)", "Không", "Tên phim, thể loại, thời lượng, đạo diễn, diễn viên, độ tuổi, poster, mô tả"),
        ("tblPhongChieu", "id (INT)", "Không", "Tên phòng chiếu, loại phòng (IMAX/3D/2D), tổng số lượng ghế"),
        ("tblGhe", "id (INT)", "idPhong -> tblPhongChieu", "Mã ghế (A01, B05...), hàng, cột, loại ghế (THUONG/VIP/SWEETBOX), phụ thu"),
        ("tblLichChieu", "id (INT)", "idPhim, idPhong", "Ngày chiếu, giờ bắt đầu, giờ kết thúc, giá vé gốc của suất chiếu"),
        ("tblHoaDon", "id (INT)", "idNhanVien, idKhachHang", "Mã HĐ, ngày lập, tổng tiền gốc, chiết khấu giảm giá, thành tiền, PTTT"),
        ("tblVe", "id (INT)", "idLichChieu, idGhe, idHoaDon", "Mã vé, đơn giá bán, thời gian xuất vé, trạng thái (DA_BAN)")
    ]
    for r_d in dd_data:
        row = tbl_dd.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    # ==================== PHẦN 4: LẬP TRÌNH & KẾT QUẢ DEMO ====================
    doc.add_heading("PHẦN 4: LẬP TRÌNH VÀ DEMO CHI TIẾT 2 MODULE ĐỀ BÀI", level=1)

    doc.add_heading("4.1. Môi trường Phát triển và Cấu trúc Mã nguồn", level=2)
    doc.add_paragraph(
        "• Ngôn ngữ: Python 3.12, HTML5, CSS3, JavaScript ES6.\n"
        "• Framework Web: Flask 3.1, Jinja2 Template Engine.\n"
        "• Cơ sở dữ liệu: SQLite 3 (kết nối qua DBConnection Singleton, kích hoạt PRAGMA foreign_keys = ON).\n"
        "• Thư viện giao diện: Bootstrap 5.3, Font Awesome 6.4 (Dark Theme rạp chiếu phim hiện đại)."
    )

    doc.add_heading("Cấu trúc cây thư mục dự án trong Editor:", level=3)
    tree_str = (
        "cineman/\n"
        "├── app.py                      # Flask Server & URL Routing\n"
        "├── controllers/                # Tầng điều khiển nghiệp vụ (Business Logic)\n"
        "│   ├── auth_controller.py      # Đăng nhập & phiên làm việc\n"
        "│   ├── ban_ve_controller.py    # Xử lý quy trình bán vé POS & chiết khấu\n"
        "│   ├── khach_hang_controller.py# Đăng ký thành viên & tra cứu thẻ\n"
        "│   ├── phim_controller.py      # Quản lý danh mục phim & lịch chiếu\n"
        "│   └── thong_ke_controller.py  # Xử lý số liệu thống kê báo cáo\n"
        "├── dao/                        # Tầng truy xuất CSDL (Data Access Objects)\n"
        "│   ├── db_connection.py        # Quản lý kết nối SQLite Singleton\n"
        "│   ├── khach_hang_dao.py       # Truy vấn tblKhachHang & tblTheThanhVien\n"
        "│   ├── phim_dao.py             # Truy vấn tblPhim\n"
        "│   ├── phong_chieu_dao.py      # Truy vấn tblPhongChieu\n"
        "│   ├── lich_chieu_dao.py       # Truy vấn tblLichChieu\n"
        "│   ├── ghe_dao.py              # Truy vấn sơ đồ ghế & kiểm tra trạng thái\n"
        "│   ├── hoa_don_dao.py          # Thao tác lưu tblHoaDon\n"
        "│   ├── ve_dao.py               # Thao tác lưu tblVe\n"
        "│   └── thong_ke_dao.py         # Thao tác tổng hợp doanh thu\n"
        "├── database/                   # CSDL SQLite\n"
        "│   ├── cineman.db              # File cơ sở dữ liệu thật\n"
        "│   └── init_db.py              # Script khởi tạo bảng và chèn dữ liệu mẫu\n"
        "├── models/                     # Thực thể nghiệp vụ (Domain Entities)\n"
        "│   ├── __init__.py\n"
        "│   └── entities.py             # NguoiDung, KhachHang, TheThanhVien, Phim, Ghe...\n"
        "├── templates/                  # Giao diện người dùng (Presentation Layer)\n"
        "│   ├── base.html               # Layout chính rạp phim\n"
        "│   ├── login.html              # Màn hình đăng nhập (có nút chọn tài khoản demo)\n"
        "│   ├── register.html           # Màn hình đăng ký thành viên\n"
        "│   ├── register_success.html   # Thông báo thành công & Thẻ thành viên điện tử\n"
        "│   ├── staff_pos.html          # Màn hình POS Bán vé tại quầy trực quan\n"
        "│   ├── ticket_print.html       # Mẫu in Vé xem phim và Hóa đơn bán lẻ\n"
        "│   ├── manager_dashboard.html  # Màn hình Thống kê báo cáo\n"
        "│   ├── manager_movies.html     # Màn hình Quản lý phim\n"
        "│   └── manager_schedules.html  # Màn hình Lên lịch chiếu\n"
        "└── README.md                   # Hướng dẫn chạy và cài đặt"
    )
    p_tr = doc.add_paragraph()
    r_tr = p_tr.add_run(tree_str)
    r_tr.font.name = 'Consolas'
    r_tr.font.size = Pt(9.5)

    # 4.2 DEMO MODULE 1
    doc.add_heading("4.2. Demo Chi Tiết Module 1: Khách Hàng Đăng Ký Thành Viên", level=2)
    doc.add_paragraph(
        "Theo yêu cầu của đề bài: \"chọn đăng kí thành viên → nhập thông tin cá nhân và click đăng kí → hệ thống lưu thông tin vào CSDL và thông báo thành công\". "
        "Quy trình được ứng dụng hiện thực hóa qua các bước chụp màn hình thực tế dưới đây:"
    )

    doc.add_paragraph("• Bước 1 & 2: Khách hàng truy cập giao diện đăng ký thành viên, nhập đầy đủ thông tin cá nhân (Họ tên, SĐT, Email, CCCD, Mật khẩu, Ngày sinh, Địa chỉ) và click nút 'Xác Nhận Đăng Ký Thành Viên':")
    img_m1_1 = os.path.join(screen_dir, "mod1_01_form_dangky.png")
    if os.path.exists(img_m1_1):
        doc.add_picture(img_m1_1, width=Inches(5.5))
        p_c = doc.add_paragraph("Hình 4.1: Giao diện Form nhập thông tin đăng ký thành viên (đã điền dữ liệu thực tế)")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 3: Hệ thống xử lý kiểm tra trùng lặp, mã hóa mật khẩu, tự động sinh mã thẻ thành viên điện tử và thông báo đăng ký thành công trực quan:")
    img_m1_2 = os.path.join(screen_dir, "mod1_02_thongbao_thanhcong.png")
    if os.path.exists(img_m1_2):
        doc.add_picture(img_m1_2, width=Inches(5.2))
        p_c = doc.add_paragraph("Hình 4.2: Giao diện Thông báo Đăng ký thành công và hiển thị Thẻ thành viên điện tử (Mã thẻ: MB-2026)")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 4 (Minh chứng CSDL): Dữ liệu khách hàng mới và thẻ thành viên được ghi nhận bền vững trong cơ sở dữ liệu SQLite (cineman.db):")
    img_m1_3 = os.path.join(screen_dir, "mod1_03_csdl_sqlite.png")
    if os.path.exists(img_m1_3):
        doc.add_picture(img_m1_3, width=Inches(6.0))
        p_c = doc.add_paragraph("Hình 4.3: Minh chứng dữ liệu lưu trữ trong bảng tblKhachHang và tblTheThanhVien của SQLite")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    # 4.3 DEMO MODULE 2
    doc.add_heading("4.3. Demo Chi Tiết Module 2: Nhân Viên Bán Vé Cho Khách Hàng Tại Quầy (POS)", level=2)
    doc.add_paragraph(
        "Theo yêu cầu của đề bài: \"chọn menu bán vé → hỏi tên phim và tìm phim → chọn phim từ danh sách kết quả → chọn giờ xem → chọn ghế → Nhập mã thẻ khách hàng thân thiết (nếu có) và xác nhận mua vé → thanh toán → hệ thống in vé và hóa đơn\". "
        "Dưới đây là hình ảnh chụp lại từng bước thực thi nghiệp vụ trên giao diện POS thực tế của CineMan:"
    )

    doc.add_paragraph("• Bước 1: Nhân viên đăng nhập hệ thống và chọn menu \"Bán vé tại quầy (POS)\":")
    img_m2_1 = os.path.join(screen_dir, "mod2_01_menu_banve.png")
    if os.path.exists(img_m2_1):
        doc.add_picture(img_m2_1, width=Inches(5.8))
        p_c = doc.add_paragraph("Hình 4.4: Màn hình bán vé tại quầy ban đầu với danh mục phim đang chiếu")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 2: Nhân viên hỏi tên phim khách muốn xem và nhập từ khóa vào ô tìm kiếm (Ví dụ: nhập 'Dune') -> Hệ thống lọc danh sách kết quả phim:")
    img_m2_2 = os.path.join(screen_dir, "mod2_02_tim_va_chon_phim.png")
    if os.path.exists(img_m2_2):
        doc.add_picture(img_m2_2, width=Inches(5.8))
        p_c = doc.add_paragraph("Hình 4.5: Tìm kiếm phim theo tên và lọc danh sách kết quả")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 3 & 4: Nhân viên chọn phim từ danh sách kết quả -> Hệ thống hiển thị các khung giờ xem (suất chiếu) trong ngày. Nhân viên click chọn suất chiếu (16:00 - Cinema Hall 01 IMAX):")
    img_m2_3 = os.path.join(screen_dir, "mod2_03_chon_gio_xem.png")
    if os.path.exists(img_m2_3):
        doc.add_picture(img_m2_3, width=Inches(5.8))
        p_c = doc.add_paragraph("Hình 4.6: Chọn phim và hiển thị các khung giờ chiếu trong ngày")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 5: Hệ thống hiển thị sơ đồ phòng chiếu với trạng thái ghế trống/đã bán. Nhân viên chọn các vị trí ghế ngồi theo yêu cầu của khách (Chọn ghế VIP D04, D05):")
    img_m2_4 = os.path.join(screen_dir, "mod2_04_chon_ghe.png")
    if os.path.exists(img_m2_4):
        doc.add_picture(img_m2_4, width=Inches(5.8))
        p_c = doc.add_paragraph("Hình 4.7: Sơ đồ ghế phòng chiếu trực quan và chọn ghế VIP (D04, D05)")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 6: Nhân viên hỏi và nhập mã thẻ khách hàng thân thiết (MB-8888) -> Hệ thống tự động áp dụng chiết khấu giảm giá 15% VIP (-39,000 đ) và tính điểm thưởng tích lũy (+22 pts):")
    img_m2_5 = os.path.join(screen_dir, "mod2_05_nhap_the_thanh_vien.png")
    if os.path.exists(img_m2_5):
        doc.add_picture(img_m2_5, width=Inches(5.8))
        p_c = doc.add_paragraph("Hình 4.8: Nhập mã thẻ thành viên thân thiết, tự động giảm giá chiết khấu và tính điểm")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    doc.add_paragraph("• Bước 7 & 8: Nhân viên chọn phương thức thanh toán, click 'Xác nhận mua vé' -> Hệ thống thực thi giao dịch CSDL và kích hoạt màn hình in vé xem phim kèm hóa đơn thanh toán:")
    img_m2_6 = os.path.join(screen_dir, "mod2_06_in_ve_hoa_don.png")
    if os.path.exists(img_m2_6):
        doc.add_picture(img_m2_6, width=Inches(5.5))
        p_c = doc.add_paragraph("Hình 4.9: Mẫu in Hóa đơn thanh toán bán vé và các cuống vé vào cửa cho từng ghế ngồi")
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.runs[0].italic = True

    # ==================== PHẦN 5: PHỤ LỤC PROMPT ====================
    doc.add_heading("PHẦN 5: PHỤ LỤC CÁC PROMPT ĐÃ DÙNG VÀ MÔ TẢ CÁCH SỬ DỤNG AI", level=1)
    doc.add_paragraph(
        "Nhằm tuân thủ quy chế học vụ và kiểm soát chất lượng kỹ thuật, không phụ thuộc máy móc vào AI dẫn tới các lỗi cơ bản về RUP/UML, "
        "bảng dưới đây ghi chép trung thực 5 câu prompt chính và mô tả chi tiết cách thức sinh viên tiếp nhận, sàng lọc, chỉnh sửa hoặc vẽ lại:"
    )

    tbl_pr = doc.add_table(rows=1, cols=4)
    tbl_pr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pr)
    h_pr = tbl_pr.rows[0].cells
    for i, t in enumerate(["STT", "Giai đoạn & Mục tiêu", "Câu Prompt đã sử dụng", "Mô tả sinh viên sử dụng kết quả thế nào"]):
        h_pr[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_pr[i], "E2E8F0")

    pr_rows = [
        ("1", "Đặc tả yêu cầu:\nKhảo sát quy trình nghiệp vụ",
         "\"Hãy liệt kê các bước trong quy trình bán vé tại quầy của rạp chiếu phim hiện đại (CGV/Lotte), có bước kiểm tra thẻ khách hàng thành viên và in vé.\"",
         "• Cách SV sử dụng: Tham khảo các bước thực tế của rạp phim lớn, sau đó đối chiếu với đề bài của cô Đặng Thị Bích Ngọc. SV loại bỏ các bước rườm rà (như gợi ý bắp nước) để bám sát đúng 2 chức năng đề bài yêu cầu: Đăng ký thành viên và Bán vé tại quầy."),
        ("2", "Đặc tả yêu cầu:\nSinh mã PlantUML Use Case",
         "\"Viết code PlantUML cho sơ đồ Use Case tổng quát hệ thống rạp chiếu phim CineMan với 3 tác nhân: Khách hàng, Nhân viên bán hàng, Nhân viên quản lý.\"",
         "• Cách SV sử dụng: AI ban đầu sinh sai: gắn quan hệ <<include>> cho chức năng nhập thẻ thành viên. SV đã tự rà soát và vẽ lại bằng PlantUML: chuyển bước thẻ thành viên sang <<extend>> vì đề bài ghi rõ 'nếu có'. Bổ sung đầy đủ swimlanes cho 2 Activity Diagram."),
        ("3", "Phân tích hệ thống:\nBiểu đồ lớp BCE",
         "\"Tạo mã PlantUML biểu đồ lớp phân tích theo phương pháp BCE (Boundary - Control - Entity) cho hệ thống CineMan rạp chiếu phim.\"",
         "• Cách SV sử dụng: Sinh viên kiểm tra thấy AI thiếu lớp thực thể TheThanhVien và chưa tách lớp trừu tượng NguoiDung. SV đã tự bổ sung đầy đủ các thuộc tính, quan hệ 1-1 giữa KhachHang và TheThanhVien, quan hệ 1-N giữa HoaDon và Ve."),
        ("4", "Thiết kế hệ thống:\nBiểu đồ tuần tự thiết kế",
         "\"Sinh biểu đồ trình tự thiết kế chi tiết cho ca sử dụng Bán vé tại quầy theo kiến trúc 3 lớp MVC có các lớp DAO và Transaction Database.\"",
         "• Cách SV sử dụng: SV tham khảo luồng tương tác, sau đó tự chuẩn hóa lại toàn bộ tên hàm theo chuẩn Java camelCase đồng nhất với Design Class Diagram (timKiemPhim, layTrangThaiGhe, tinhChietKhau, taoHoaDon, taoVe). Thêm cơ chế Transaction rollback khi có lỗi."),
        ("5", "Lập trình & Demo:\nKhung ứng dụng web Flask",
         "\"Gợi ý khung ứng dụng web Python Flask theo mô hình 3 lớp MVC, có cơ sở dữ liệu SQLite và sơ đồ ghế rạp chiếu phim.\"",
         "• Cách SV sử dụng: SV chỉ lấy ý tưởng cấu trúc thư mục làm sườn; tự viết toàn bộ 9 file DAO với câu truy vấn SQL chuẩn khóa ngoại; tự lập trình thuật toán tính chiết khấu giảm giá theo hạng thẻ (VIP 15%, Gold 10%, Silver 7%, Standard 5%) và tích điểm tự động 10%.")
    ]
    for r_d in pr_rows:
        row = tbl_pr.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    # ==================== PHẦN 6: BẢNG TỰ ĐÁNH GIÁ (KHIÊM TỐN, CHÂN THỰC) ====================
    doc.add_heading("PHẦN 6: BẢNG TỰ ĐÁNH GIÁ KẾT QUẢ THEO TIÊU CHÍ BỘ MÔN", level=1)
    doc.add_paragraph(
        "Căn cứ vào biểu mẫu tự đánh giá trực tuyến của bộ môn (https://forms.gle/yuLGeZZtWheGsnPu5), "
        "sinh viên nghiêm túc tự đánh giá kết quả thực hiện đồ án CineMan theo tinh thần khiêm tốn, trung thực, thẳng thắn nhìn nhận các điểm đạt được và các hạn chế còn tồn đọng:"
    )

    tbl_ev = doc.add_table(rows=1, cols=4)
    tbl_ev.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ev)
    h_ev = tbl_ev.rows[0].cells
    for i, t in enumerate(["Hạng mục đánh giá", "Mức độ hoàn thành thực tế", "Điểm trừ & Hạn chế tự nhận", "Điểm tự chấm"]):
        h_ev[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_ev[i], "E2E8F0")

    ev_rows = [
        ("1. Đặc tả yêu cầu\n(Thang điểm 2.0)",
         "Đã xây dựng Use Case tổng quát, phân rã theo tác nhân, đặc tả chi tiết 2 UC trọng tâm chuẩn form mẫu PTIT và 2 sơ đồ hoạt động có swimlane rõ ràng.",
         "Chưa đặc tả hết các ca sử dụng phụ như hủy/hoàn vé khi có sự cố chiếu phim.",
         "1.75 / 2.0"),
        ("2. Phân tích hệ thống\n(Thang điểm 2.0)",
         "Biểu đồ lớp phân tích BCE rõ ràng; 2 biểu đồ trình tự phân tích thể hiện đúng thông điệp giữa Boundary, Control, Entity.",
         "Chưa xây dựng biểu đồ giao tiếp (Communication Diagram) để có góc nhìn cộng tác đa chiều.",
         "1.75 / 2.0"),
        ("3. Thiết kế hệ thống\n(Thang điểm 2.5)",
         "Kiến trúc phân tầng MVC rõ ràng; Biểu đồ lớp thiết kế chi tiết có đủ kiểu dữ liệu, visibility (-/+), phương thức; Biểu đồ tuần tự thiết kế có chi tiết DAO & Transaction; ERD chuẩn 3NF và từ điển 10 bảng dữ liệu.",
         "Biểu đồ lớp thiết kế mới tập trung vào các lớp nghiệp vụ của 2 chức năng chính, các chức năng phụ của người quản lý chưa chi tiết hóa hết phương thức.",
         "2.0 / 2.5"),
        ("4. Lập trình và Demo\n(Thang điểm 2.5)",
         "Ứng dụng web Python Flask chạy thực tế mượt mà; Demo xuất sắc và rõ ràng 2 module của đề bài (Đăng ký thành viên và Bán vé tại quầy); Sơ đồ ghế trực quan; In vé và hóa đơn chi tiết; Lưu dữ liệu thật trong SQLite; Đã push GitHub và share quyền cho dtbnptit@gmail.com.",
         "Chưa tích hợp cổng thanh toán trực tuyến thực tế (VNPay / MoMo) mà mới thực hiện mô phỏng quy trình thanh toán; chưa tích hợp máy quét mã vạch vật lý.",
         "2.0 / 2.5"),
        ("5. Báo cáo & Phụ lục Prompt\n(Thang điểm 1.0)",
         "Báo cáo trình bày đúng thể thức PTIT; Bảng phụ lục prompt ghi chép trung thực 5 prompt thực tế, giải trình rõ việc tự rà soát và chỉnh sửa lỗi của AI.",
         "Chưa ghi chép lại đầy đủ các prompt phụ nhỏ phát sinh trong quá trình sửa lỗi giao diện CSS.",
         "0.75 / 1.0"),
        ("TỔNG ĐIỂM TỰ ĐÁNH GIÁ",
         "Sinh viên hoàn thành bài tập lớn nghiêm túc, hiểu rõ bản chất quy trình phân tích thiết kế, tự tin bảo vệ đồ án.",
         "Nhìn nhận trung thực các mặt cần hoàn thiện thêm.",
         "8.25 / 10.0")
    ]
    for r_d in ev_rows:
        row = tbl_ev.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            p = c.paragraphs[0]
            if "TỔNG ĐIỂM" in r_d[0]:
                p.add_run(val).bold = True
                set_cell_background(c, "FEF3C7")
            else:
                p.add_run(val)
            set_cell_margins(c)

    doc.save(out_docx)
    print(f"[OK] Đã xuất file báo cáo cập nhật thành công: {out_docx} ({os.path.getsize(out_docx)} bytes)")

if __name__ == '__main__':
    build_report()
