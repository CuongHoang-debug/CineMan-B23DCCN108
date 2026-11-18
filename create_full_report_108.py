import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    # Người dùng yêu cầu: không để màu bảng (tất cả các ô nền trắng / trong suốt)
    pass

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="000000"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_heading_with_spacing(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.name = 'Times New Roman'
        r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_image_figure(doc, img_path, caption, width_inch=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inch))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        rc = p_cap.add_run(caption)
        rc.italic = True
        rc.font.size = Pt(10.5)
        rc.font.color.rgb = RGBColor(0, 0, 0)
    else:
        p_warn = doc.add_paragraph(f"[Ảnh: {caption} - Chưa tìm thấy file]")
        p_warn.alignment = WD_ALIGN_PARAGRAPH.CENTER

def build_report():
    doc = Document()

    # Cấu hình Style Normal
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12.5)
    font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    # Cấu hình toàn bộ Headings sang chữ đen mặc định
    for h_name in ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
        if h_name in doc.styles:
            h_style = doc.styles[h_name]
            h_style.font.name = 'Times New Roman'
            h_style.font.color.rgb = RGBColor(0, 0, 0)

    uml_dir = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\uml_108"
    screen_dir = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\screenshots"
    out_docx = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\reports\14B23DCCN108.docx"
    out_docx_d22 = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\reports\14D22DCCN108.docx"
    out_docx_b23 = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\reports\14B23DCCN108.docx"
    cover_img_path = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\cover_fixed_v3.png"

    # ==================== TRANG BÌA (CHUẨN FORM MẪU BỘ MÔN TIN HỌC CƠ SỞ / PTIT) ====================
    # ...
    # (Trang bìa được vẽ từ ảnh cover_108_hires.png, thông tin lớp không có trên ảnh này)
    # ...
    # Phần nội dung bên dưới, tìm và xóa các đoạn thêm Lớp nếu có
    # ...

    # ==================== ĐỀ BÀI & CÁC LINK NỘP ====================
    add_heading_with_spacing(doc, "NỘI DUNG ĐỀ BÀI VÀ CÁC ĐƯỜNG LINK NỘP BÀI", level=1)
    
    doc.add_heading("1. Nội dung đề bài (Đề 14 - CineMan):", level=2)
    p_req = doc.add_paragraph()
    p_req.add_run(
        "\"Một hệ thống quản lý rạp chiếu phim (CineMan) cho phép nhân viên quản lí, nhân viên bán hàng và khách hàng sử dụng. "
        "Sau khi đăng nhập, các tác nhân có thể thực hiện:\n"
        "• Nhân viên quản lí: xem các loại thống kê: phim, khách hàng và doanh thu. Lên lịch chiếu, quản lí thông tin phim, phòng chiếu (thêm, sửa, xóa).\n"
        "• Nhân viên bán hàng: bán vé tại quầy cho khách hàng, xuất thẻ thành viên cho khách hàng.\n"
        "• Khách hàng: đăng kí thành viên, tìm kiếm, mua vé trực tuyến, mua vé tại quầy.\n"
        "• Chức năng khách hàng đăng kí thành viên: chọn đăng kí thành viên → nhập thông tin cá nhân và click đăng kí → hệ thống lưu thông tin vào CSDL và thông báo thành công.\n"
        "• Chức năng nhân viên bán vé cho khách hàng (tại quầy): chọn menu bán vé → hỏi tên phim và tìm phim → chọn phim từ danh sách kết quả → chọn giờ xem → chọn ghế → Nhập mã thẻ khách hàng thân thiết (nếu có) và xác nhận mua vé → thanh toán → hệ thống in vé và hóa đơn.\"\n"
    ).italic = True

    doc.add_heading("2. Bảng tổng hợp các đường link nộp bài trực tuyến của bộ môn:", level=2)
    tbl_links = doc.add_table(rows=1, cols=3)
    tbl_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_links)
    hl = tbl_links.rows[0].cells
    hl[0].paragraphs[0].add_run("STT").bold = True
    hl[1].paragraphs[0].add_run("Hạng mục nộp bài").bold = True
    hl[2].paragraphs[0].add_run("Đường link Google Form / GitHub").bold = True
    set_cell_background(hl[0], "E2E8F0")
    set_cell_background(hl[1], "E2E8F0")
    set_cell_background(hl[2], "E2E8F0")

    link_data = [
        ("1", "Nộp code PlantUML phần Đặc tả", "https://forms.gle/WjBeCqMYZnMPHmcV7 (File: cineman_form_dacta_108.puml)"),
        ("2", "Nộp code PlantUML phần Phân tích", "https://forms.gle/ciKQDmZntpPKuH4H7 (File: cineman_form_phantich_108.puml)"),
        ("3", "Nộp code PlantUML phần Thiết kế", "https://forms.gle/rqmj7ZFnfQ5n7FzD7 (File: cineman_form_thietke_108.puml)"),
        ("4", "Nộp Form tự đánh giá bài làm", "https://forms.gle/yuLGeZZtWheGsnPu5 (Tự đánh giá: 8.25/10.0)"),
        ("5", "Kho mã nguồn dự án (GitHub)", "https://github.com/cuonghm108/CineMan-B23DCCN108\n(Đã chia sẻ quyền Collaborator cho: dtbnptit@gmail.com)")
    ]
    for r_d in link_data:
        row = tbl_links.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    doc.add_page_break()

    # ==================== PHẦN A: ĐẶC TẢ ====================
    add_heading_with_spacing(doc, "PHẦN A: ĐẶC TẢ YÊU CẦU HỆ THỐNG", level=1)

    add_heading_with_spacing(doc, "1. Bảng Từ Khóa (3 Nhóm Đối Tượng)", level=2)
    doc.add_paragraph("Dựa trên văn bản mô tả bài toán, hệ thống CineMan trích xuất và phân loại các từ khóa thành 3 nhóm cơ bản:")

    tbl_kw = doc.add_table(rows=1, cols=4)
    tbl_kw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_kw)
    h_kw = tbl_kw.rows[0].cells
    for i, t in enumerate(["Nhóm từ khóa", "Từ khóa (Tiếng Việt)", "Thuật ngữ kỹ thuật (English)", "Ghi chú vai trò"]):
        h_kw[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_kw[i], "E2E8F0")

    kw_rows = [
        ("Nhóm 1: Con người", "Khách hàng", "Customer", "Người mua vé xem phim, đăng ký thành viên tích điểm"),
        ("Nhóm 1: Con người", "Nhân viên bán hàng", "Sales Staff / Cashier", "Thực hiện bán vé tại quầy, xuất thẻ thành viên"),
        ("Nhóm 1: Con người", "Nhân viên quản lý", "Manager", "Quản lý phim, phòng chiếu, lên lịch chiếu và xem thống kê"),
        ("Nhóm 1: Con người", "Người dùng chung", "User", "Tác nhân khái quát đại diện cho tài khoản đăng nhập"),
        ("Nhóm 2: Hoạt động con người", "Đăng nhập", "Login", "Xác thực danh tính và phân quyền truy cập chức năng"),
        ("Nhóm 2: Hoạt động con người", "Đăng ký thành viên", "Register Member", "Khách hàng khai báo thông tin để nhận thẻ thành viên"),
        ("Nhóm 2: Hoạt động con người", "Bán vé tại quầy (POS)", "Sell Ticket At Counter", "Quy trình bán vé trực tiếp cho khách hàng tại quầy"),
        ("Nhóm 2: Hoạt động con người", "Xuất thẻ thành viên", "Issue Member Card", "Cấp phát thẻ thành viên vật lý / điện tử tại quầy"),
        ("Nhóm 2: Hoạt động con người", "Tìm kiếm phim", "Search Movie", "Tra cứu phim theo tên hoặc thể loại"),
        ("Nhóm 2: Hoạt động con người", "Mua vé trực tuyến", "Book Ticket Online", "Khách hàng tự đặt vé qua giao diện web"),
        ("Nhóm 2: Hoạt động con người", "Quản lý phim", "Manage Movies", "Thêm mới, sửa đổi thông tin hoặc ngừng chiếu phim"),
        ("Nhóm 2: Hoạt động con người", "Quản lý phòng chiếu", "Manage Auditoriums", "Thêm phòng, cấu hình sơ đồ ghế và loại phòng"),
        ("Nhóm 2: Hoạt động con người", "Lên lịch chiếu", "Schedule Showtime", "Sắp xếp suất chiếu theo phim, phòng và khung giờ"),
        ("Nhóm 2: Hoạt động con người", "Xem thống kê", "View Statistics", "Theo dõi doanh thu, số lượng vé và điểm khách hàng"),
        ("Nhóm 3: Vật / Đối tượng", "Phim", "Movie", "Tác phẩm điện ảnh chiếu tại rạp với thời lượng, đạo diễn"),
        ("Nhóm 3: Vật / Đối tượng", "Phòng chiếu", "Auditorium / Cinema Room", "Không gian chiếu phim chứa các hàng ghế (IMAX, 3D, 2D)"),
        ("Nhóm 3: Vật / Đối tượng", "Ghế", "Seat", "Vị trí ngồi trong phòng chiếu (Ghế thường, VIP, Sweetbox)"),
        ("Nhóm 3: Vật / Đối tượng", "Suất chiếu (Giờ xem)", "Showtime", "Khung giờ cụ thể chiếu một bộ phim tại phòng chiếu nhất định"),
        ("Nhóm 3: Vật / Đối tượng", "Vé xem phim", "Ticket", "Chứng từ xác nhận quyền vào xem phim cho một ghế"),
        ("Nhóm 3: Vật / Đối tượng", "Hóa đơn", "Invoice / Bill", "Chứng từ thanh toán tổng hợp tiền vé và chiết khấu"),
        ("Nhóm 3: Vật / Đối tượng", "Thẻ thành viên", "Membership Card", "Thẻ chứa mã số, hạng thẻ và điểm thưởng tích lũy"),
        ("Nhóm 3: Vật / Đối tượng", "Báo cáo thống kê", "Report / Statistics", "Tài liệu tổng hợp số liệu doanh thu, lượt xem")
    ]
    for r_d in kw_rows:
        row = tbl_kw.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "2. Bảng Giải Thích Ngữ Nghĩa Chi Tiết Khái Niệm (24 Khái Niệm)", level=2)
    tbl_sem = doc.add_table(rows=1, cols=3)
    tbl_sem.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_sem)
    h_sem = tbl_sem.rows[0].cells
    h_sem[0].paragraphs[0].add_run("STT").bold = True
    h_sem[1].paragraphs[0].add_run("Khái niệm").bold = True
    h_sem[2].paragraphs[0].add_run("Giải thích ngữ nghĩa chi tiết trong bài toán CineMan").bold = True
    set_cell_background(h_sem[0], "E2E8F0")
    set_cell_background(h_sem[1], "E2E8F0")
    set_cell_background(h_sem[2], "E2E8F0")

    sem_data = [
        ("1", "Khách hàng", "Người sử dụng dịch vụ xem phim tại rạp. Có thể là khách vãng lai hoặc khách hàng thân thiết đã có thẻ thành viên. Có quyền đăng ký tài khoản, tìm phim, đặt vé online hoặc mua vé trực tiếp tại quầy."),
        ("2", "Nhân viên bán hàng", "Nhân sự trực tiếp làm việc tại quầy vé (POS). Có nhiệm vụ tư vấn tên phim, tra cứu suất chiếu, chọn ghế trên sơ đồ theo ý khách, áp dụng thẻ thành viên giảm giá, thu tiền và in vé + hóa đơn."),
        ("3", "Nhân viên quản lý", "Người có quyền hạn cao trong rạp chiếu phim. Chịu trách nhiệm lập kế hoạch lịch chiếu, cập nhật danh mục phim đang chiếu, bảo trì thông tin phòng chiếu và theo dõi các báo cáo thống kê doanh thu."),
        ("4", "Người dùng (User chung)", "Khái niệm tổng quát bao hàm Nhân viên quản lý, Nhân viên bán hàng và Khách hàng. Mỗi người dùng có một tài khoản xác thực bằng tên đăng nhập và mật khẩu."),
        ("5", "Đăng nhập", "Hành động người dùng nhập tên đăng nhập và mật khẩu để hệ thống xác thực danh tính và điều hướng tới giao diện chức năng phù hợp theo vai trò quyền hạn."),
        ("6", "Đăng ký thành viên", "Quy trình khách hàng khai báo thông tin cá nhân (Họ tên, SĐT, Email, CCCD, Mật khẩu, Ngày sinh, Địa chỉ) vào hệ thống để được cấp mã thẻ thành viên điện tử và điểm tích lũy khởi tạo."),
        ("7", "Bán vé tại quầy (POS)", "Quy trình nghiệp vụ cốt lõi tại quầy vé gồm: hỏi phim -> tìm kiếm -> chọn phim -> chọn suất chiếu -> chọn ghế ngồi -> áp dụng thẻ thành viên nếu có -> thanh toán -> in vé và hóa đơn."),
        ("8", "Xuất thẻ thành viên", "Thao tác của nhân viên tại quầy cấp thẻ vật lý hoặc mã số thẻ mới cho khách hàng đăng ký trực tiếp tại rạp."),
        ("9", "Tìm kiếm phim", "Chức năng cho phép nhập từ khóa (tên phim, diễn viên) để hệ thống lọc ra danh sách các phim phù hợp đang được phát hành tại rạp."),
        ("10", "Mua vé trực tuyến", "Quy trình khách hàng tự thao tác chọn suất chiếu, ghế ngồi và thanh toán qua cổng điện tử trên trang web của rạp."),
        ("11", "Quản lý phim", "Tập hợp các thao tác Thêm, Sửa, Xóa danh mục phim. Lưu trữ thông tin poster, thời lượng, thể loại, đạo diễn, giới hạn độ tuổi và mô tả."),
        ("12", "Quản lý phòng chiếu", "Thao tác cấu hình phòng chiếu bao gồm tên phòng, loại công nghệ chiếu (IMAX, 3D, 2D) và ma trận bố trí ghế ngồi (số hàng, số cột, loại ghế)."),
        ("13", "Lên lịch chiếu", "Nghiệp vụ sắp xếp khung thời gian bắt đầu và kết thúc của một phim trong một phòng chiếu cụ thể vào ngày nhất định, không được trùng giờ."),
        ("14", "Xem thống kê", "Chức năng tổng hợp số liệu kinh doanh theo nhiều chiều: doanh thu theo ngày/tháng, số vé bán theo phim, và mức độ tích lũy điểm của khách hàng."),
        ("15", "Phim", "Đối tượng dữ liệu thể hiện một bộ phim được chiếu tại rạp. Thuộc tính gồm mã phim, tên phim, thể loại, thời lượng (phút), đạo diễn, ngày khởi chiếu."),
        ("16", "Phòng chiếu", "Không gian vật lý tổ chức chiếu phim. Thuộc tính gồm mã phòng, tên phòng, loại phòng và tổng sức chứa ghế."),
        ("17", "Ghế", "Vị trí ngồi của khách trong phòng chiếu. Có tọa độ hàng-cột (như D04, D05), loại ghế (Thường, VIP, Đôi/Sweetbox) và phụ thu tương ứng."),
        ("18", "Suất chiếu", "Một lần chiếu phim xác định bởi: mã suất chiếu, phim được chiếu, phòng chiếu, ngày chiếu, giờ bắt đầu, giờ kết thúc và đơn giá vé gốc."),
        ("19", "Vé xem phim", "Chứng từ xác nhận quyền vào phòng chiếu cho đúng một vị trí ghế trong một suất chiếu cụ thể. Trạng thái gồm 'ĐÃ BÁN', 'HỦY'."),
        ("20", "Hóa đơn", "Chứng từ tài chính ghi nhận một giao dịch mua bán vé gồm: mã hóa đơn, nhân viên lập, khách hàng mua, tổng tiền gốc, tiền giảm giá, thành tiền và thời gian lập."),
        ("21", "Thẻ thành viên", "Đối tượng liên kết với khách hàng gồm mã thẻ (MB-XXXX), hạng thẻ (VIP, Gold, Silver, Standard), ngày cấp và số điểm tích lũy."),
        ("22", "Thống kê doanh thu", "Báo cáo tài chính phản ánh tổng tiền vé thu được theo khoảng thời gian tùy chọn (ngày, tuần, tháng, quý)."),
        ("23", "Thống kê phim", "Báo cáo xếp hạng mức độ ăn khách của các bộ phim dựa trên số lượng vé bán ra và doanh thu thực thu."),
        ("24", "Thống kê khách hàng", "Báo cáo phân loại khách hàng theo thứ hạng thành viên, tần suất mua vé và điểm thưởng tích lũy.")
    ]
    for r_d in sem_data:
        row = tbl_sem.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "3. Mô Tả Hệ Thống (Chuẩn Luồng Nghiệp Vụ --->)", level=2)
    doc.add_heading("3.1. Mục đích hệ thống:", level=3)
    doc.add_paragraph(
        "Hệ thống CineMan được xây dựng nhằm tin học hóa và tự động hóa toàn diện quy trình vận hành rạp chiếu phim hiện đại: "
        "từ khâu tiếp đón khách hàng, tra cứu thông tin phim, chọn chỗ ngồi trực quan, thanh toán nhanh chóng tại quầy POS, "
        "cho đến công tác quản lý hậu cần như lập lịch chiếu phim, quản lý danh mục phim, quản lý cấu hình phòng chiếu và cung cấp báo cáo thống kê trực quan cho ban quản lý."
    )

    doc.add_heading("3.2. Phạm vi hệ thống:", level=3)
    doc.add_paragraph(
        "Phạm vi bao gồm ứng dụng web tương thích trên thiết bị quầy vé bán hàng POS, giao diện web công cộng cho khách hàng đăng ký và tra cứu, "
        "cùng giao diện dashboard quản trị cho nhân viên quản lý rạp. Hệ thống tập trung giải quyết trọn vẹn 2 module nghiệp vụ trọng tâm được giao trong đề bài."
    )

    doc.add_heading("3.3. Hoạt động nghiệp vụ các chức năng (Mô tả theo luồng mũi tên --->):", level=3)
    flows = [
        ("Chức năng Đăng nhập:",
         "Người dùng nhập tên đăng nhập và mật khẩu ---> Hệ thống kiểm tra hợp lệ dữ liệu ---> Hệ thống truy vấn CSDL xác thực thông tin và quyền hạn ---> Hệ thống khởi tạo phiên làm việc (Session) ---> Hệ thống điều hướng tới giao diện chính tương ứng (Quản lý / Bán hàng / Khách hàng)."),
        ("Chức năng Khách hàng đăng ký thành viên (Module 1):",
         "Khách hàng chọn menu Đăng ký thành viên ---> Hệ thống hiển thị biểu mẫu đăng ký ---> Khách hàng nhập thông tin cá nhân (Họ tên, SĐT, Email, CCCD, Mật khẩu, Ngày sinh, Địa chỉ) và click Đăng ký ---> Hệ thống kiểm tra định dạng dữ liệu và tính duy nhất của Email, SĐT, CCCD trong CSDL ---> Hệ thống lưu trữ thông tin khách hàng vào CSDL ---> Hệ thống tự động khởi tạo bản ghi thẻ thành viên mới với mã thẻ MB-XXXX và điểm tích lũy = 0 ---> Hệ thống hiển thị giao diện thông báo đăng ký thành công kèm thông tin thẻ thành viên điện tử."),
        ("Chức năng Nhân viên bán vé tại quầy cho khách hàng (Module 2):",
         "Nhân viên đăng nhập thành công và chọn menu Bán vé tại quầy ---> Hệ thống hiển thị giao diện bán vé POS với ô tìm kiếm và danh mục phim ---> Nhân viên hỏi tên phim khách muốn xem và nhập vào ô tìm kiếm ---> Hệ thống lọc danh sách kết quả phim phù hợp ---> Nhân viên chọn phim từ danh sách kết quả ---> Hệ thống truy vấn và hiển thị danh sách các suất chiếu (khung giờ xem) trong ngày của phim đó ---> Khách chọn giờ xem, nhân viên click chọn suất chiếu tương ứng ---> Hệ thống truy xuất CSDL và hiển thị sơ đồ ghế của phòng chiếu với trạng thái từng ghế (trống / đã bán) và loại ghế (Thường / VIP / Đôi) ---> Khách hàng chọn vị trí ghế, nhân viên click chọn các ghế tương ứng trên sơ đồ ---> Hệ thống cập nhật bảng tóm tắt đơn hàng và tổng tiền vé tạm tính ---> Nhân viên hỏi khách hàng mã thẻ thân thiết. Nếu khách có thẻ, nhân viên nhập mã thẻ và nhấn Áp dụng ---> Hệ thống tra cứu thẻ thành viên trong CSDL, xác định hạng thẻ và tự động áp dụng chiết khấu giảm giá cùng điểm thưởng tích lũy ---> Khách hàng thực hiện thanh toán ---> Nhân viên chọn hình thức thanh toán và nhấn Xác nhận mua vé & In hóa đơn ---> Hệ thống khởi tạo Giao dịch CSDL: cập nhật trạng thái các ghế đã chọn sang ĐÃ BÁN, tạo bản ghi Hóa đơn, tạo các bản ghi Vé, cộng điểm thưởng vào thẻ thành viên ---> Hệ thống kích hoạt lệnh in vé xem phim và hóa đơn thanh toán giao cho khách hàng."),
        ("Chức năng Xuất thẻ thành viên tại quầy:",
         "Nhân viên chọn menu Xuất thẻ thành viên ---> Hệ thống hiển thị form nhập thông tin khách hàng ---> Nhân viên nhập thông tin của khách và nhấn Cấp thẻ ---> Hệ thống kiểm tra tính duy nhất, lưu CSDL và in thẻ thành viên cho khách hàng."),
        ("Chức năng Quản lý phim:",
         "Nhân viên quản lý chọn Quản lý phim ---> Hệ thống hiển thị danh sách phim hiện có ---> Quản lý chọn Thêm phim mới (hoặc Sửa/Xóa) ---> Quản lý nhập thông tin chi tiết phim và nhấn Lưu ---> Hệ thống xác thực và cập nhật dữ liệu vào bảng Phim trong CSDL."),
        ("Chức năng Quản lý phòng chiếu:",
         "Nhân viên quản lý chọn Quản lý phòng chiếu ---> Hệ thống hiển thị danh sách phòng và sức chứa ---> Quản lý chọn Thêm phòng hoặc Cấu hình sơ đồ ghế ---> Hệ thống lưu thiết lập phòng và tạo ma trận ghế vào CSDL."),
        ("Chức năng Lên lịch chiếu:",
         "Nhân viên quản lý chọn Lên lịch chiếu ---> Hệ thống hiển thị thời khóa biểu chiếu phim ---> Quản lý chọn Phim, chọn Phòng chiếu, chọn Ngày và Giờ bắt đầu ---> Hệ thống kiểm tra xung đột khung giờ chiếu trong cùng phòng ---> Nếu hợp lệ, hệ thống lưu suất chiếu mới vào CSDL."),
        ("Chức năng Xem thống kê:",
         "Nhân viên quản lý chọn menu Thống kê ---> Quản lý chọn loại thống kê (Theo phim / Khách hàng / Doanh thu) và khoảng thời gian ---> Hệ thống tính toán, tổng hợp số liệu từ các bảng Hóa đơn, Vé và biểu diễn dạng bảng số liệu và biểu đồ trực quan.")
    ]
    for title, content in flows:
        p_fl = doc.add_paragraph()
        p_fl.add_run(f"• {title}\n").bold = True
        p_fl.add_run(content)

    doc.add_heading("3.4. Thông tin đối tượng trong hệ thống:", level=3)
    doc.add_paragraph(
        "• Phim: mã phim, tên phim, thể loại, thời lượng, đạo diễn, diễn viên, ngày khởi chiếu, độ tuổi quy định, poster, tóm tắt nội dung.\n"
        "• Phòng chiếu: mã phòng, tên phòng chiếu, loại phòng chiếu (IMAX, 3D, 2D), tổng số hàng ghế, tổng số cột ghế, sức chứa.\n"
        "• Ghế: mã ghế, vị trí hàng, vị trí cột, loại ghế (Ghế Thường, Ghế VIP, Ghế Sweetbox), phụ thu theo loại ghế.\n"
        "• Suất chiếu: mã suất chiếu, mã phim, mã phòng chiếu, ngày chiếu, giờ bắt đầu, giờ kết thúc, giá vé niêm yết cơ sở.\n"
        "• Vé: mã vé, mã suất chiếu, mã ghế, mã hóa đơn, đơn giá bán thực tế, trạng thái vé (Đã bán, Hủy), ngày xuất vé.\n"
        "• Hóa đơn: mã hóa đơn, mã nhân viên lập, mã khách hàng, ngày giờ lập, tổng tiền vé gốc, chiết khấu giảm giá, số tiền thanh toán thực tế, phương thức thanh toán.\n"
        "• Thẻ thành viên: mã thẻ (MB-XXXX), mã khách hàng, hạng thẻ (VIP, Gold, Silver, Standard), điểm thưởng tích lũy, ngày kích hoạt.\n"
        "• Khách hàng: mã khách hàng, họ và tên, số điện thoại, địa chỉ email, số căn cước công dân (CCCD), ngày sinh, địa chỉ thường trú.\n"
        "• Nhân viên: mã nhân viên, họ và tên, chức vụ, số điện thoại, tài khoản hệ thống, mật khẩu đăng nhập, ca làm việc."
    )

    doc.add_heading("3.5. Bảng quan hệ thông tin giữa các thực thể:", level=3)
    tbl_rel = doc.add_table(rows=1, cols=4)
    tbl_rel.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_rel)
    hr = tbl_rel.rows[0].cells
    for i, t in enumerate(["Thực thể nguồn", "Bản số quan hệ", "Thực thể đích", "Mô tả ngữ nghĩa quan hệ"]):
        hr[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(hr[i], "E2E8F0")

    rel_rows = [
        ("Phim", "1 - N", "Suất chiếu", "Một bộ phim có thể được lên lịch chiếu ở nhiều suất chiếu khác nhau."),
        ("Phòng chiếu", "1 - N", "Suất chiếu", "Một phòng chiếu phục vụ nhiều suất chiếu theo các khung giờ khác nhau."),
        ("Phòng chiếu", "1 - N", "Ghế", "Một phòng chiếu sở hữu nhiều vị trí ghế ngồi được bố trí theo ma trận hàng-cột."),
        ("Suất chiếu", "1 - N", "Vé", "Một suất chiếu có thể phát hành nhiều vé xem phim cho các vị trí ghế khác nhau."),
        ("Ghế", "1 - N", "Vé", "Một chiếc ghế có thể được bán trong nhiều suất chiếu khác nhau (mỗi suất 1 vé)."),
        ("Hóa đơn", "1 - N", "Vé", "Một hóa đơn bán hàng có thể chứa nhiều vé xem phim của cùng một giao dịch mua."),
        ("Nhân viên", "1 - N", "Hóa đơn", "Một nhân viên bán hàng có thể lập nhiều hóa đơn cho các khách hàng tại quầy."),
        ("Khách hàng", "0/1 - N", "Hóa đơn", "Một khách hàng có thể mua vé và phát sinh nhiều hóa đơn thanh toán."),
        ("Khách hàng", "1 - 1", "Thẻ thành viên", "Mỗi khách hàng đăng ký thành viên được liên kết duy nhất với một thẻ thành viên.")
    ]
    for r_d in rel_rows:
        row = tbl_rel.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "4. Biểu Đồ Ca Sử Dụng Tổng Quan (Use Case Diagram 108)", level=2)
    doc.add_paragraph(
        "Sơ đồ ca sử dụng tổng quan thể hiện toàn bộ ranh giới hệ thống CineMan, 3 tác nhân chính (Khách hàng, Nhân viên bán hàng, Nhân viên quản lý) "
        "và các ca sử dụng chức năng nghiệp vụ tương ứng:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "01_usecase_tongquan_108.png"), "Hình 1.1: Sơ đồ Ca sử dụng Tổng quan Hệ thống CineMan (108)")

    doc.add_heading("Bảng mô tả tóm tắt các ca sử dụng trong sơ đồ tổng quan:", level=3)
    tbl_uc_all = doc.add_table(rows=1, cols=4)
    tbl_uc_all.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_uc_all)
    h_ua = tbl_uc_all.rows[0].cells
    for i, t in enumerate(["Mã UC", "Tác nhân chính", "Tên ca sử dụng", "Mục đích nghiệp vụ"]):
        h_ua[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_ua[i], "E2E8F0")

    ua_rows = [
        ("UC00_108", "Tác nhân chung", "Đăng nhập hệ thống", "Xác thực danh tính người dùng và phân quyền truy cập."),
        ("UC01_108", "Khách hàng", "Đăng ký thành viên", "Khách hàng khai báo thông tin cá nhân và nhận mã thẻ thành viên điện tử."),
        ("UC02_108", "Khách hàng", "Tìm kiếm phim & suất chiếu", "Tra cứu thông tin phim đang chiếu và khung giờ chiếu tại rạp."),
        ("UC03_108", "Khách hàng", "Mua vé trực tuyến", "Khách hàng tự thao tác chọn ghế và đặt vé qua website."),
        ("UC04_108", "Nhân viên bán hàng", "Bán vé tại quầy (POS)", "Quy trình bán vé trực tiếp cho khách hàng tại quầy vé."),
        ("UC05_108", "Nhân viên bán hàng", "Xuất thẻ thành viên", "Cấp phát thẻ thành viên mới cho khách hàng trực tiếp tại quầy."),
        ("UC06_108", "Nhân viên quản lý", "Quản lý phim", "Thêm, cập nhật thông tin phim hoặc ngừng chiếu."),
        ("UC07_108", "Nhân viên quản lý", "Quản lý phòng chiếu", "Quản lý danh sách phòng và cấu hình sơ đồ ghế."),
        ("UC08_108", "Nhân viên quản lý", "Lên lịch chiếu", "Sắp xếp suất chiếu theo phim, phòng chiếu và khung giờ."),
        ("UC09_108", "Nhân viên quản lý", "Xem thống kê báo cáo", "Xem báo cáo doanh thu, số lượng vé theo phim và khách hàng.")
    ]
    for r_d in ua_rows:
        row = tbl_uc_all.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "5. Biểu Đồ Ca Sử Dụng Chi Tiết Cho 2 Module Trọng Tâm (108)", level=2)
    doc.add_heading("5.1. Ca sử dụng chi tiết: Khách hàng đăng ký thành viên (UC01_108)", level=3)
    doc.add_paragraph(
        "Sơ đồ ca sử dụng phân rã chi tiết quá trình khách hàng đăng ký thành viên, gồm quan hệ <<include>> kiểm tra thông tin hợp lệ "
        "và quan hệ <<extend>> thông báo lỗi khi thông tin bị trùng lặp:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "02_usecase_chitiet_dangky_108.png"), "Hình 1.2: Sơ đồ Ca sử dụng Chi tiết - Đăng ký thành viên (108)")

    doc.add_heading("5.2. Ca sử dụng chi tiết: Nhân viên bán vé tại quầy (UC04_108)", level=3)
    doc.add_paragraph(
        "Sơ đồ ca sử dụng phân rã chi tiết toàn bộ các bước nghiệp vụ bán vé tại quầy của nhân viên: từ tìm kiếm phim, chọn suất chiếu, "
        "chọn ghế ngồi, <<extend>> nhập thẻ thành viên thân thiết (nếu có), thanh toán và in vé + hóa đơn:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "03_usecase_chitiet_banve_108.png"), "Hình 1.3: Sơ đồ Ca sử dụng Chi tiết - Bán vé tại quầy POS (108)")

    doc.add_page_break()

    # ==================== PHẦN B: PHÂN TÍCH ====================
    add_heading_with_spacing(doc, "PHẦN B: PHA PHÂN TÍCH HỆ THỐNG", level=1)

    add_heading_with_spacing(doc, "1. Kịch Bản v1 (Bảng Đặc Tả Kịch Bản Nghiệp Vụ)", level=2)
    doc.add_heading("1.1. Kịch bản v1: Ca sử dụng Đăng ký thành viên (108)", level=3)

    tbl_kb1 = doc.add_table(rows=7, cols=2)
    tbl_kb1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_kb1)
    kb1_data = [
        ("Mã ca sử dụng:", "UC01_108 - Khách hàng đăng ký thành viên"),
        ("Tác nhân:", "Khách hàng (Customer)"),
        ("Tiền điều kiện:", "Khách hàng truy cập vào trang chủ CineMan, chưa đăng nhập hệ thống."),
        ("Hậu điều kiện:", "Thông tin khách hàng được lưu vào CSDL; hệ thống sinh mã thẻ `MB-XXXX`, cấp hạng Standard, điểm = 0."),
        ("Kịch bản chính\n(Các bước thực hiện):",
         "1. Khách hàng bấm chọn liên kết \"Đăng ký thành viên\" trên thanh điều hướng.\n"
         "2. Hệ thống hiển thị Form đăng ký thành viên gồm các trường thông tin: Họ và tên, Số điện thoại, Email, Số CCCD, Mật khẩu, Ngày sinh, Địa chỉ.\n"
         "3. Khách hàng điền đầy đủ các thông tin và click nút \"Xác nhận Đăng ký\".\n"
         "4. Hệ thống kiểm tra tính hợp lệ của dữ liệu: định dạng email chuẩn, SĐT 10 số, CCCD 12 số, mật khẩu tối thiểu 6 ký tự.\n"
         "5. Hệ thống truy vấn CSDL kiểm tra tính duy nhất: SĐT, Email và CCCD chưa từng được đăng ký trước đó.\n"
         "6. Hệ thống mã hóa mật khẩu, ghi bản ghi mới vào bảng Khách hàng trong CSDL.\n"
         "7. Hệ thống tự động tạo bản ghi Thẻ thành viên liên kết với khách hàng, sinh mã thẻ ngẫu nhiên duy nhất (ví dụ: MB-2026), khởi tạo điểm thưởng = 0.\n"
         "8. Hệ thống hiển thị thông báo: \"Đăng ký thành viên thành công!\", trình bày thẻ thành viên điện tử kèm mã thẻ để khách hàng lưu lại.\n"
         "9. Ca sử dụng kết thúc."),
        ("Khung giao diện mô phỏng\n(Mockup):",
         "+-----------------------------------------------------------------------+\n"
         "| [CineMan]   TRANG ĐĂNG KÝ THÀNH VIÊN                                  |\n"
         "| Họ và tên:      [ Hoàng Mạnh Cường                                   ]|\n"
         "| Số điện thoại:  [ 0987654321                                         ]|\n"
         "| Email:          [ cuonghm108@gmail.com                               ]|\n"
         "| Số CCCD:        [ 001203009999                                       ]|\n"
         "| Mật khẩu:       [ ********                                           ]|\n"
         "| Ngày sinh:      [ 20/05/2005                                         ]|\n"
         "| Địa chỉ:        [ Hà Đông, Hà Nội                                    ]|\n"
         "|                 [  XÁC NHẬN ĐĂNG KÝ THÀNH VIÊN  ]                     |\n"
         "+-----------------------------------------------------------------------+"),
        ("Ngoại lệ:",
         "• 4a. Thiếu trường thông tin bắt buộc hoặc định dạng không hợp lệ: Hệ thống giữ nguyên các dữ liệu đã nhập, bôi đỏ trường lỗi và yêu cầu nhập lại.\n"
         "• 5a. Số điện thoại, Email hoặc CCCD đã tồn tại trong hệ thống: Hệ thống hiển thị thông báo lỗi 'Tài khoản đã tồn tại' và gợi ý đăng nhập.")
    ]
    for idx, (lbl, val) in enumerate(kb1_data):
        row = tbl_kb1.rows[idx]
        row.cells[0].paragraphs[0].add_run(lbl).bold = True
        row.cells[0].width = Inches(1.8)
        row.cells[1].paragraphs[0].add_run(val)
        row.cells[1].width = Inches(4.2)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])

    doc.add_heading("1.2. Kịch bản v1: Ca sử dụng Bán vé cho khách hàng tại quầy (108)", level=3)
    tbl_kb2 = doc.add_table(rows=7, cols=2)
    tbl_kb2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_kb2)
    kb2_data = [
        ("Mã ca sử dụng:", "UC04_108 - Nhân viên bán vé cho khách hàng tại quầy (POS)"),
        ("Tác nhân:", "Nhân viên bán hàng (Cashier), Khách hàng (Customer)"),
        ("Tiền điều kiện:", "Nhân viên bán hàng đã đăng nhập vào hệ thống; hệ thống rạp có suất chiếu trong ngày."),
        ("Hậu điều kiện:", "Hóa đơn và các vé được lưu vào CSDL; trạng thái ghế chuyển sang ĐÃ BÁN; cộng điểm thẻ thành viên; in vé và hóa đơn."),
        ("Kịch bản chính\n(Các bước thực hiện):",
         "1. Nhân viên bán hàng chọn menu \"Bán vé tại quầy (POS)\".\n"
         "2. Hệ thống hiển thị màn hình bán vé với danh mục phim và thanh tìm kiếm phim.\n"
         "3. Nhân viên hỏi tên phim khách muốn xem và nhập tên phim vào ô tìm kiếm.\n"
         "4. Hệ thống lọc danh sách và hiển thị các phim khớp với từ khóa tìm kiếm.\n"
         "5. Nhân viên click chọn bộ phim mà khách hàng yêu cầu.\n"
         "6. Hệ thống hiển thị danh sách các suất chiếu (khung giờ xem) trong ngày của bộ phim đó.\n"
         "7. Khách hàng chọn giờ xem; nhân viên click chọn suất chiếu tương ứng.\n"
         "8. Hệ thống tải và hiển thị sơ đồ phòng chiếu với trạng thái từng vị trí ghế (Ghế trống / Ghế đã bán; phân biệt màu ghế Thường, VIP, Đôi).\n"
         "9. Khách hàng chỉ định vị trí ghế ngồi; nhân viên click chọn các ghế tương ứng trên màn hình cảm ứng.\n"
         "10. Hệ thống cập nhật danh sách ghế đã chọn và tính toán tổng tiền vé tạm thời.\n"
         "11. Nhân viên hỏi khách hàng: 'Quý khách có thẻ thành viên CineMan không?'.\n"
         "12. Nếu có, nhân viên nhập mã thẻ thành viên (ví dụ: MB-8888) vào ô và bấm nút \"Áp dụng\".\n"
         "13. Hệ thống kiểm tra thẻ thành viên, hiển thị thông tin chủ thẻ, hạng thẻ và tự động trừ chiết khấu giảm giá (VIP 15%, Gold 10%, Silver 7%, Standard 5%) đồng thời hiển thị điểm tích lũy dự kiến.\n"
         "14. Nhân viên thông báo tổng số tiền cần thanh toán cho khách hàng.\n"
         "15. Khách hàng thực hiện thanh toán tiền (Tiền mặt / Chuyển khoản QR / Thẻ ngân hàng).\n"
         "16. Nhân viên chọn hình thức thanh toán và click nút \"Xác nhận mua vé & In hóa đơn\".\n"
         "17. Hệ thống thực hiện lưu giao dịch CSDL: đổi trạng thái ghế sang ĐÃ BÁN, tạo bản ghi Hóa đơn, tạo bản ghi Vé, cộng điểm tích lũy vào thẻ khách hàng.\n"
         "18. Hệ thống in vé xem phim và hóa đơn thanh toán giao cho khách hàng.\n"
         "19. Ca sử dụng kết thúc."),
        ("Khung giao diện mô phỏng\n(Mockup):",
         "+-----------------------------------------------------------------------+\n"
         "| [CineMan POS]  BÁN VÉ TẠI QUẦY                                        |\n"
         "| Tìm phim: [ Dune: Part Two           ] [Tìm kiếm]                     |\n"
         "| DS Phim:  (o) Dune: Part Two (166') | ( ) Mai (131') | ( ) Kung Fu... |\n"
         "| Suất chiếu trong ngày: [ 16:00 - Cinema Hall 01 IMAX ]                 |\n"
         "| Sơ đồ ghế:                                                            |\n"
         "|   [Màn hình chiếu IMAX]                                               |\n"
         "|   Hàng D: [D01] [D02] [D03] [*D04*] [*D05*] [D06(Đã bán)]             |\n"
         "| Ghế đã chọn: D04 (VIP), D05 (VIP) | Tạm tính: 260,000 đ               |\n"
         "| Thẻ thành viên: [ MB-8888          ] [Áp dụng] -> Giảm 15%: -39,000 đ |\n"
         "| TỔNG CỘNG THANH TOÁN: 221,000 đ                                       |\n"
         "| Phương thức: [x] Tiền mặt  [ ] Chuyển khoản QR                        |\n"
         "|             [  XÁC NHẬN MUA VÉ & IN HÓA ĐƠN  ]                        |\n"
         "+-----------------------------------------------------------------------+"),
        ("Ngoại lệ:",
         "• 4a. Không tìm thấy phim khớp từ khóa: Hệ thống báo 'Không có phim phù hợp', nhân viên tư vấn khách chọn phim khác trong danh mục đang chiếu.\n"
         "• 9a. Ghế khách chọn vừa bị hệ thống bán cho khách khác: Hệ thống cảnh báo ghế đã có người đặt, yêu cầu chọn vị trí khác.\n"
         "• 12a. Mã thẻ thành viên không tồn tại: Hệ thống báo lỗi thẻ không hợp lệ và tiếp tục thanh toán theo giá vé gốc.")
    ]
    for idx, (lbl, val) in enumerate(kb2_data):
        row = tbl_kb2.rows[idx]
        row.cells[0].paragraphs[0].add_run(lbl).bold = True
        row.cells[0].width = Inches(1.8)
        row.cells[1].paragraphs[0].add_run(val)
        row.cells[1].width = Inches(4.2)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])

    add_heading_with_spacing(doc, "2. Trích Lớp Thực Thể Từ Văn Bản Mô Tả (Quy Trình 5 Bước Chuẩn)", level=2)
    doc.add_heading("Bước 1: Trích tập danh từ từ văn bản mô tả bài toán:", level=3)
    doc.add_paragraph(
        "Tập danh từ được trích xuất: hệ thống, rạp chiếu phim, nhân viên quản lý, nhân viên bán hàng, khách hàng, "
        "thống kê, phim, doanh thu, lịch chiếu, phòng chiếu, vé, quầy, thẻ thành viên, thông tin cá nhân, CSDL, "
        "tên phim, kết quả, giờ xem, ghế, mã thẻ khách hàng thân thiết, thanh toán, hóa đơn, tài khoản, mật khẩu."
    )

    doc.add_heading("Bước 2: Đánh giá và phân loại danh từ:", level=3)
    tbl_eval = doc.add_table(rows=1, cols=4)
    tbl_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_eval)
    he = tbl_eval.rows[0].cells
    for i, t in enumerate(["Danh từ trích xuất", "Phân loại", "Lý do chấp nhận / Loại trừ", "Kết luận thực thể"]):
        he[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(he[i], "E2E8F0")

    eval_data = [
        ("Khách hàng", "Thực thể", "Tác nhân quan trọng có thuộc tính định danh, thông tin cá nhân và thẻ", "Khachhang108"),
        ("Nhân viên bán hàng", "Thực thể", "Tác nhân thực hiện giao dịch bán vé tại quầy, lập hóa đơn", "Nhanvien108"),
        ("Nhân viên quản lý", "Thực thể", "Tác nhân quản lý danh mục và điều hành lịch chiếu", "Nhanvien108"),
        ("Phim", "Thực thể", "Đối tượng độc lập có thông tin tên, thể loại, thời lượng, đạo diễn", "Phim108"),
        ("Phòng chiếu", "Thực thể", "Đối tượng độc lập đại diện không gian chiếu, chứa các ghế", "Phongchieu108"),
        ("Ghế", "Thực thể", "Vị trí ngồi cụ thể có tọa độ, loại ghế và đơn giá phụ thu", "Ghe108"),
        ("Suất chiếu (Lịch)", "Thực thể", "Thời điểm phát hành một phim trong một phòng chiếu cụ thể", "Suatchieu108"),
        ("Vé", "Thực thể", "Chứng từ xác nhận đặt chỗ cho từng ghế trong một suất chiếu", "Ve108"),
        ("Hóa đơn", "Thực thể", "Chứng từ giao dịch tài chính ghi nhận thanh toán", "Hoadon108"),
        ("Thẻ thành viên", "Thực thể", "Thẻ tích điểm gắn liền với khách hàng thân thiết", "Thethanhvien108"),
        ("Tên phim, giờ xem", "Thuộc tính", "Là đặc tính thuộc về thực thể Phim và Suất chiếu", "Loại trừ (Thuộc tính)"),
        ("Thông tin cá nhân", "Thuộc tính", "Gồm họ tên, SĐT, email, CCCD thuộc về Khách hàng", "Loại trừ (Thuộc tính)"),
        ("Hệ thống, CSDL, quầy", "Khái niệm", "Môi trường kỹ thuật và địa điểm vật lý, không quản lý thông tin", "Bỏ qua")
    ]
    for r_d in eval_data:
        row = tbl_eval.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    doc.add_heading("Bước 3: Xác định quan hệ số lượng giữa các lớp thực thể:", level=3)
    doc.add_paragraph(
        "• Phim108 (1) — (0..*) Suatchieu108: Một bộ phim có thể có nhiều suất chiếu hoặc chưa có suất nào.\n"
        "• Phongchieu108 (1) — (0..*) Suatchieu108: Một phòng chiếu có thể được xếp lịch cho nhiều suất chiếu.\n"
        "• Phongchieu108 (1) — (1..*) Ghe108: Một phòng chiếu chứa nhiều ghế ngồi.\n"
        "• Suatchieu108 (1) — (0..*) Ve108: Một suất chiếu có thể phát hành nhiều vé xem phim.\n"
        "• Ghe108 (1) — (0..*) Ve108: Mỗi chiếc ghế trong một suất chiếu ứng với tối đa 1 vé.\n"
        "• Hoadon108 (1) — (1..*) Ve108: Một hóa đơn chứa 1 hoặc nhiều vé xem phim được thanh toán cùng lúc.\n"
        "• Nhanvien108 (1) — (0..*) Hoadon108: Một nhân viên bán hàng có thể lập nhiều hóa đơn bán vé.\n"
        "• Khachhang108 (0..1) — (0..*) Hoadon108: Khách hàng có thể có nhiều hóa đơn (hoặc khách vãng lai).\n"
        "• Khachhang108 (1) — (1) Thethanhvien108: Mỗi khách hàng đăng ký có đúng một thẻ thành viên."
    )

    doc.add_heading("Bước 4: Sơ đồ quan hệ đối tượng & Bước 5: Bảng thuộc tính chi tiết từng thực thể:", level=3)
    tbl_ent_attr = doc.add_table(rows=1, cols=4)
    tbl_ent_attr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ent_attr)
    hea = tbl_ent_attr.rows[0].cells
    for i, t in enumerate(["Tên lớp thực thể (108)", "Thuộc tính (Private)", "Kiểu dữ liệu", "Mô tả ngữ nghĩa"]):
        hea[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(hea[i], "E2E8F0")

    attr_data = [
        ("Phim108", "id, tenPhim, theLoai, thoiLuong, daoDien, moTa", "int, String, String, int, String, String", "Lưu trữ thông tin chi tiết phim đang chiếu tại rạp"),
        ("Phongchieu108", "id, tenPhong, loaiPhong, tongSoGhe", "int, String, String, int", "Quản lý phòng chiếu (IMAX, 3D, 2D) và số lượng ghế"),
        ("Ghe108", "id, idPhong, maGhe, hang, cot, loaiGhe, phuThu", "int, int, String, String, int, String, float", "Vị trí ghế (A01, D04), phân loại Thường/VIP/Đôi"),
        ("Suatchieu108", "id, idPhim, idPhong, ngayChieu, gioBatDau, giaVeGoc", "int, int, int, Date, Time, float", "Thời điểm phát hành phim cụ thể tại một phòng"),
        ("Ve108", "id, idSuatChieu, idGhe, idHoaDon, giaBan, trangThai", "int, int, int, int, float, String", "Vé xem phim xác nhận đặt ghế, trạng thái DA_BAN"),
        ("Hoadon108", "id, idNhanVien, idKhachHang, ngayLap, tongTien, giamGia, thanhTien", "int, int, int, Timestamp, float, float, float", "Hóa đơn thanh toán bán vé kèm chiết khấu"),
        ("Thethanhvien108", "id, idKhachHang, maThe, hangThe, diemTichLuy", "int, int, String, String, int", "Thẻ thành viên (MB-XXXX), tích lũy điểm thưởng"),
        ("Khachhang108", "id, hoTen, sdt, email, cccd, ngaySinh, diaChi", "int, String, String, String, String, Date, String", "Thông tin khách hàng hội viên của CineMan"),
        ("Nhanvien108", "id, hoTen, taiKhoan, matKhau, vaiTro, sdt", "int, String, String, String, String, String", "Nhân viên bán hàng / Quản lý vận hành rạp")
    ]
    for r_d in attr_data:
        row = tbl_ent_attr.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "3. Sơ Đồ Lớp Thực Thể Toàn Hệ Thống (Entity Class Diagram 108)", level=2)
    doc.add_paragraph(
        "Sơ đồ lớp thực thể biểu diễn toàn diện các thực thể dữ liệu nghiệp vụ của rạp chiếu phim CineMan cùng thuộc tính và mối liên kết:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "04_entity_class_diagram_108.png"), "Hình 2.1: Sơ đồ Lớp Thực thể Toàn Hệ thống CineMan (108)")

    add_heading_with_spacing(doc, "4. Trích Lớp Phân Tích Cho 2 Module (Boundary - Entity 108)", level=2)
    doc.add_heading("4.1. Biểu đồ lớp phân tích: Module Bán vé tại quầy (108)", level=3)
    doc.add_paragraph(
        "Biểu đồ phân tích cấu trúc màn hình giao diện (Boundary) và liên kết với các lớp thực thể (Entity) trong quy trình bán vé tại quầy:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "05_analysis_class_banve_108.png"), "Hình 2.2: Biểu đồ Lớp Phân tích - Ca sử dụng Bán vé tại quầy (108)")

    doc.add_heading("4.2. Biểu đồ lớp phân tích: Module Đăng ký thành viên (108)", level=3)
    doc.add_paragraph(
        "Biểu đồ phân tích thể hiện các thành phần giao diện nhập liệu, kết quả và thực thể khách hàng, thẻ thành viên:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "14_analysis_class_dangky_108.png"), "Hình 2.3: Biểu đồ Lớp Phân tích - Ca sử dụng Đăng ký thành viên (108)")

    add_heading_with_spacing(doc, "5. Phân Tích Hoạt Động (Kịch Bản v2, Biểu Đồ Giao Tiếp & Trình Tự)", level=2)
    doc.add_heading("5.1. Kịch bản v2: Phân tích tương tác đối tượng cho Module Bán vé tại quầy (108)", level=3)
    doc.add_paragraph(
        "Kịch bản v2 mô tả rõ ràng thông điệp truyền nhận giữa Actor, các giao diện Boundary và các thực thể Entity:\n"
        "1. Nhân viên tương tác với `GDChinhNVBH108` -> Chọn 'Bán vé tại quầy'.\n"
        "2. `GDChinhNVBH108` gọi mở giao diện `GDChonPhim108`.\n"
        "3. `GDChonPhim108` truy vấn `Phim108` lấy danh sách phim đang chiếu và hiển thị lên màn hình.\n"
        "4. Nhân viên chọn phim -> `GDChonPhim108` gọi mở `GDChonSuatChieu108`.\n"
        "5. `GDChonSuatChieu108` gọi `Suatchieu108` lấy các khung giờ chiếu trong ngày và hiển thị.\n"
        "6. Nhân viên chọn suất chiếu -> `GDChonSuatChieu108` gọi mở `GDChonGhe108`.\n"
        "7. `GDChonGhe108` gọi `Ghe108` lấy sơ đồ ghế và trạng thái trống/bán -> hiển thị trực quan.\n"
        "8. Nhân viên chọn vị trí ghế -> `GDChonGhe108` gọi mở giao diện `GDThanhToan108`.\n"
        "9. `GDThanhToan108` nhận mã thẻ thành viên -> gọi `Thethanhvien108` tính chiết khấu -> hiển thị tổng thanh toán.\n"
        "10. Nhân viên xác nhận thanh toán -> `GDThanhToan108` gọi `Hoadon108` lưu hóa đơn và tạo vé -> in vé và hóa đơn hoàn tất."
    )

    doc.add_heading("5.2. Biểu đồ giao tiếp (Communication Diagrams 108):", level=3)
    doc.add_paragraph("Biểu đồ giao tiếp thể hiện kiến trúc cộng tác mạng lưới giữa các đối tượng phân tích:")
    add_image_figure(doc, os.path.join(uml_dir, "06_communication_banve_108.png"), "Hình 2.4: Biểu đồ Giao tiếp (Communication) - Ca sử dụng Bán vé tại quầy (108)")
    add_image_figure(doc, os.path.join(uml_dir, "15_communication_dangky_108.png"), "Hình 2.5: Biểu đồ Giao tiếp (Communication) - Ca sử dụng Đăng ký thành viên (108)")

    doc.add_heading("5.3. Biểu đồ trình tự phân tích (Sequence Analysis Diagrams 108):", level=3)
    doc.add_paragraph("Biểu đồ trình tự phân tích diễn giải dòng thời gian trao đổi thông điệp nghiệp vụ:")
    add_image_figure(doc, os.path.join(uml_dir, "07_sequence_analysis_banve_108.png"), "Hình 2.6: Biểu đồ Trình tự Phân tích - Ca sử dụng Bán vé tại quầy (108)")
    add_image_figure(doc, os.path.join(uml_dir, "16_sequence_analysis_dangky_108.png"), "Hình 2.7: Biểu đồ Trình tự Phân tích - Ca sử dụng Đăng ký thành viên (108)")

    doc.add_page_break()

    # ==================== PHẦN C: THIẾT KẾ ====================
    add_heading_with_spacing(doc, "PHẦN C: PHA THIẾT KẾ HỆ THỐNG", level=1)

    add_heading_with_spacing(doc, "1. Thiết Kế Cơ Sở Dữ Liệu Quan Hệ (108)", level=2)
    doc.add_paragraph(
        "Lược đồ CSDL quan hệ được thiết kế chuẩn hóa đạt chuẩn dạng 3 (3NF), đảm bảo toàn vẹn dữ liệu và tối ưu hóa hiệu năng truy vấn giao dịch:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "08_database_schema_108.png"), "Hình 3.1: Lược đồ Cơ sở Dữ liệu Quan hệ Chuẩn 3NF (108)")

    doc.add_heading("Từ điển dữ liệu chi tiết các bảng trong CSDL:", level=3)
    tbl_td = doc.add_table(rows=1, cols=4)
    tbl_td.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_td)
    htd = tbl_td.rows[0].cells
    for i, t in enumerate(["Tên Bảng CSDL", "Khóa chính (PK)", "Khóa ngoại (FK)", "Vai trò lưu trữ nghiệp vụ"]):
        htd[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(htd[i], "E2E8F0")

    td_rows = [
        ("tblNguoiDung108", "id (INTEGER)", "Không", "Lưu thông tin đăng nhập, mật khẩu mã hóa, vai trò (Admin, Staff, Customer)"),
        ("tblKhachHang108", "id (INTEGER)", "id -> tblNguoiDung108", "Lưu CCCD, ngày sinh, địa chỉ thường trú của khách hàng"),
        ("tblTheThanhVien108", "id (INTEGER)", "idKhachHang -> tblKhachHang108", "Mã thẻ thành viên (MB-XXXX), hạng thẻ, điểm tích lũy"),
        ("tblPhim108", "id (INTEGER)", "Không", "Tên phim, thể loại, thời lượng, đạo diễn, poster, trạng thái chiếu"),
        ("tblPhongChieu108", "id (INTEGER)", "Không", "Tên phòng chiếu, loại công nghệ (IMAX/3D/2D), tổng số ghế"),
        ("tblGhe108", "id (INTEGER)", "idPhong -> tblPhongChieu108", "Mã ghế (A01, D04), vị trí hàng, cột, loại ghế (Thường/VIP/Đôi), phụ thu"),
        ("tblSuatChieu108", "id (INTEGER)", "idPhim, idPhong", "Ngày chiếu, giờ bắt đầu, giờ kết thúc, đơn giá vé cơ bản"),
        ("tblHoaDon108", "id (INTEGER)", "idNhanVien, idKhachHang", "Mã hóa đơn, ngày lập, tổng tiền, chiết khấu thẻ, số tiền thực thu, PTTT"),
        ("tblVe108", "id (INTEGER)", "idSuatChieu, idGhe, idHoaDon", "Mã vé, đơn giá vé bán ra, thời gian in vé, trạng thái (DA_BAN)")
    ]
    for r_d in td_rows:
        row = tbl_td.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "2. Thiết Kế Chi Tiết Biểu Đồ Lớp (Design Class Diagram 108)", level=2)
    doc.add_paragraph(
        "Biểu đồ lớp thiết kế chi tiết tuân thủ mô hình kiến trúc MVC / DAO đặc trưng của hệ thống thông tin hướng đối tượng:\n"
        "• Tầng View / Boundary: Các trang giao diện (`GDChonPhim108.jsp`, `GDChonSuatChieu108.jsp`, `GDChonGhe108.jsp`, `GDThanhToan108.jsp`, `GDDangKy108.jsp`...).\n"
        "• Tầng DAO (Data Access Object): `Phim108DAO`, `Suatchieu108DAO`, `Ghe108DAO`, `Hoadon108DAO`, `Ve108DAO`, `Khachhang108DAO`, `Thethanhvien108DAO` thực thi các câu lệnh SQL.\n"
        "• Tầng Model / Entity: `Phim108`, `Suatchieu108`, `Ghe108`, `Hoadon108`, `Ve108`, `Khachhang108`, `Thethanhvien108` chứa dữ liệu và phương thức getter/setter."
    )
    doc.add_heading("2.1. Biểu đồ lớp thiết kế: Module Bán vé tại quầy (108)", level=3)
    add_image_figure(doc, os.path.join(uml_dir, "09_design_class_banve_108.png"), "Hình 3.2: Biểu đồ Lớp Thiết kế Chi tiết - Ca sử dụng Bán vé tại quầy (108)")

    doc.add_heading("2.2. Biểu đồ lớp thiết kế: Module Đăng ký thành viên (108)", level=3)
    add_image_figure(doc, os.path.join(uml_dir, "17_design_class_dangky_108.png"), "Hình 3.3: Biểu đồ Lớp Thiết kế Chi tiết - Ca sử dụng Đăng ký thành viên (108)")

    add_heading_with_spacing(doc, "3. Thiết Kế Biểu Đồ Hoạt Động (Activity Diagram 108)", level=2)
    doc.add_paragraph(
        "Biểu đồ hoạt động sử dụng swimlanes (làn bơi) phân định trách nhiệm rõ ràng giữa Người dùng, Giao diện hệ thống và Cơ sở dữ liệu:"
    )
    doc.add_heading("3.1. Biểu đồ hoạt động: Module Bán vé tại quầy (108)", level=3)
    add_image_figure(doc, os.path.join(uml_dir, "10_activity_banve_108.png"), "Hình 3.4: Biểu đồ Hoạt động (Activity Diagram) - Ca sử dụng Bán vé tại quầy (108)")

    doc.add_heading("3.2. Biểu đồ hoạt động: Module Đăng ký thành viên (108)", level=3)
    add_image_figure(doc, os.path.join(uml_dir, "18_activity_dangky_108.png"), "Hình 3.5: Biểu đồ Hoạt động (Activity Diagram) - Ca sử dụng Đăng ký thành viên (108)")

    add_heading_with_spacing(doc, "4. Thiết Kế Biểu Đồ Tuần Tự (Kịch Bản v3 & Sequence Design 108)", level=2)
    doc.add_heading("4.1. Kịch bản v3: Đặc tả phương thức gọi giữa các lớp kỹ thuật", level=3)
    doc.add_paragraph(
        "Kịch bản v3 xác định chính xác tên phương thức, đối số truyền vào và đối tượng DAO tương ứng:\n"
        "• Bán vé: `timKiemPhim(keyword)` -> `Phim108DAO.getPhimTheoTen()` -> `getSuatChieuTheoPhim(idPhim)` -> `Suatchieu108DAO.getSuatChieu()` -> `getDanhSachGhe(idPhong, idSuat)` -> `Ghe108DAO.getTrangThaiGhe()` -> `kiemTraThe(maThe)` -> `Thethanhvien108DAO.getThe()` -> `luuHoaDon(hoaDon)` -> `Hoadon108DAO.insert()` -> `luuVe(dsVe)` -> `Ve108DAO.insertBatch()`.\n"
        "• Đăng ký: `dangKyThanhVien(khachHang)` -> `Khachhang108DAO.kiemTraTrungLap()` -> `Khachhang108DAO.insert()` -> `Thethanhvien108DAO.taoTheMoi(idKH, maThe)`."
    )
    doc.add_heading("4.2. Biểu đồ tuần tự thiết kế: Module Bán vé tại quầy (108)", level=3)
    add_image_figure(doc, os.path.join(uml_dir, "11_sequence_design_banve_108.png"), "Hình 3.6: Biểu đồ Tuần tự Thiết kế Chi tiết - Ca sử dụng Bán vé tại quầy (108)")

    doc.add_heading("4.3. Biểu đồ tuần tự thiết kế: Module Đăng ký thành viên (108)", level=3)
    add_image_figure(doc, os.path.join(uml_dir, "19_sequence_design_dangky_108.png"), "Hình 3.7: Biểu đồ Tuần tự Thiết kế Chi tiết - Ca sử dụng Đăng ký thành viên (108)")

    add_heading_with_spacing(doc, "5. Biểu Đồ Gói & Biểu Đồ Triển Khai (108)", level=2)
    doc.add_heading("5.1. Biểu đồ gói kiến trúc hệ thống (Package Diagram 108)", level=3)
    doc.add_paragraph(
        "Biểu đồ gói mô tả sự phân tách trách nhiệm giữa tầng Giao diện (view / jsp), tầng Điều khiển (controller), "
        "tầng Truy cập dữ liệu (dao), tầng Thực thể (model / entity) và CSDL nền tảng:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "12_package_diagram_108.png"), "Hình 3.8: Biểu đồ Gói Kiến trúc Hệ thống (Package Diagram 108)")

    doc.add_heading("5.2. Biểu đồ triển khai vật lý (Deployment Diagram 108)", level=3)
    doc.add_paragraph(
        "Biểu đồ triển khai thể hiện các nút phần cứng (Hardware Nodes) và các thành phần phần mềm (Artifacts) khi hệ thống vận hành thực tế:"
    )
    add_image_figure(doc, os.path.join(uml_dir, "13_deployment_diagram_108.png"), "Hình 3.9: Biểu đồ Triển khai Vật lý Hệ thống (Deployment Diagram 108)")

    doc.add_page_break()

    # ==================== PHẦN D: LẬP TRÌNH & DEMO ====================
    add_heading_with_spacing(doc, "PHẦN D: LẬP TRÌNH VÀ KẾT QUẢ DEMO THỰC TẾ", level=1)

    add_heading_with_spacing(doc, "1. Môi Trường Công Nghệ Và Cấu Trúc File Dự Án", level=2)
    doc.add_paragraph(
        "• Ngôn ngữ lập trình: Python 3.12, HTML5, CSS3, JavaScript ES6.\n"
        "• Kiến trúc ứng dụng: 3 lớp chuẩn MVC (Model - View - Controller) kết hợp DAO Pattern.\n"
        "• Web Framework: Flask 3.1 & Jinja2 Template Engine.\n"
        "• Cơ sở dữ liệu: SQLite 3 (`cineman.db`) với đầy đủ ràng buộc khóa ngoại `PRAGMA foreign_keys = ON`.\n"
        "• Giao diện: Bootstrap 5.3 Dark Theme phong cách rạp chiếu phim hiện đại, Font Awesome 6.4."
    )

    doc.add_heading("Cấu trúc file dự án trong IDE / Editor:", level=3)
    tree_str = (
        "cineman_project/\n"
        "├── src/\n"
        "│   ├── app.py                      # Flask App Controller & Web Routes\n"
        "│   ├── controllers/                # Tầng Controller điều phối nghiệp vụ\n"
        "│   │   ├── auth_controller.py      # Đăng nhập & phiên làm việc Session\n"
        "│   │   ├── ban_ve_controller.py    # Xử lý quy trình bán vé POS & giảm giá\n"
        "│   │   ├── khach_hang_controller.py# Đăng ký thành viên & tra cứu thẻ\n"
        "│   │   ├── phim_controller.py      # Quản lý phim & suất chiếu\n"
        "│   │   └── thong_ke_controller.py  # Tổng hợp doanh thu & số vé\n"
        "│   ├── dao/                        # Tầng DAO truy xuất CSDL\n"
        "│   │   ├── db_connection.py        # Quản lý kết nối SQLite Singleton\n"
        "│   │   ├── khach_hang_dao.py       # DAO bảng Khách hàng & Thẻ thành viên\n"
        "│   │   ├── phim_dao.py             # DAO bảng Phim\n"
        "│   │   ├── phong_chieu_dao.py      # DAO bảng Phòng chiếu\n"
        "│   │   ├── lich_chieu_dao.py       # DAO bảng Suất chiếu\n"
        "│   │   ├── ghe_dao.py              # DAO bảng Ghế & kiểm tra trạng thái trống/bán\n"
        "│   │   ├── hoa_don_dao.py          # DAO bảng Hóa đơn bán vé\n"
        "│   │   └── ve_dao.py               # DAO bảng Vé xem phim\n"
        "│   ├── database/                   # Cơ sở dữ liệu SQLite\n"
        "│   │   ├── cineman.db              # File cơ sở dữ liệu thật\n"
        "│   │   └── init_db.py              # Script khởi tạo bảng & dữ liệu ban đầu\n"
        "│   ├── models/                     # Tầng Model định nghĩa thực thể\n"
        "│   │   └── entities.py             # NguoiDung, KhachHang, TheThanhVien, Phim, Ghe...\n"
        "│   └── templates/                  # Giao diện Presentation HTML/Jinja2\n"
        "│       ├── base.html               # Layout rạp chiếu phim chung\n"
        "│       ├── register.html           # Màn hình Form đăng ký thành viên\n"
        "│       ├── register_success.html   # Màn hình Thông báo đăng ký thành công\n"
        "│       ├── staff_pos.html          # Màn hình POS bán vé tại quầy trực quan\n"
        "│       ├── ticket_print.html       # Mẫu in Vé xem phim và Hóa đơn bán lẻ\n"
        "│       └── login.html              # Màn hình Đăng nhập hệ thống\n"
        "├── uml_108/                        # Toàn bộ 19 file mã nguồn PlantUML suffix 108\n"
        "└── reports/                        # Báo cáo đồ án nộp bài (11B23DCCN108.docx)"
    )
    p_tr = doc.add_paragraph()
    r_tr = p_tr.add_run(tree_str)
    r_tr.font.name = 'Consolas'
    r_tr.font.size = Pt(9.5)

    add_heading_with_spacing(doc, "2. Demo Chi Tiết Module 1: Khách Hàng Đăng Ký Thành Viên", level=2)
    doc.add_paragraph(
        "Hiện thực hóa yêu cầu của đề bài: \"chọn đăng kí thành viên → nhập thông tin cá nhân và click đăng kí → hệ thống lưu thông tin vào CSDL và thông báo thành công\". "
        "Dưới đây là chuỗi hình ảnh chụp trực tiếp từ ứng dụng thực tế:"
    )

    doc.add_paragraph("• Bước 1 & 2: Khách hàng truy cập trang web, điền thông tin cá nhân (Họ tên: Hoàng Mạnh Cường, SĐT: 0987654321, Email: cuonghm108@gmail.com, CCCD: 001203009999) và bấm nút 'Xác Nhận Đăng Ký Thành Viên':")
    add_image_figure(doc, os.path.join(screen_dir, "mod1_01_form_dangky.png"), "Hình 4.1: Giao diện Form nhập thông tin đăng ký thành viên thực tế (Module 1)")

    doc.add_paragraph("• Bước 3: Hệ thống xử lý kiểm tra hợp lệ, ghi CSDL, tự động cấp mã thẻ thành viên điện tử (Mã thẻ: MB-2026) và hiển thị thông báo thành công trực quan:")
    add_image_figure(doc, os.path.join(screen_dir, "mod1_02_thongbao_thanhcong.png"), "Hình 4.2: Giao diện Thông báo Đăng ký thành công & Thẻ thành viên điện tử được cấp")

    doc.add_paragraph("• Bước 4 (Minh chứng CSDL): Bản ghi khách hàng mới và thẻ thành viên được lưu trữ bền vững trong cơ sở dữ liệu SQLite (`cineman.db`):")
    add_image_figure(doc, os.path.join(screen_dir, "mod1_03_csdl_sqlite.png"), "Hình 4.3: Minh chứng dữ liệu được ghi nhận trong bảng tblKhachHang và tblTheThanhVien")

    add_heading_with_spacing(doc, "3. Demo Chi Tiết Module 2: Nhân Viên Bán Vé Tại Quầy (POS)", level=2)
    doc.add_paragraph(
        "Hiện thực hóa yêu cầu của đề bài: \"chọn menu bán vé → hỏi tên phim và tìm phim → chọn phim từ danh sách kết quả → chọn giờ xem → chọn ghế → Nhập mã thẻ khách hàng thân thiết (nếu có) và xác nhận mua vé → thanh toán → hệ thống in vé và hóa đơn\". "
        "Dưới đây là các bước chụp màn hình thực tế trên giao diện bán vé POS:"
    )

    doc.add_paragraph("• Bước 1: Nhân viên đăng nhập vào hệ thống và chọn menu \"Bán vé tại quầy (POS)\":")
    add_image_figure(doc, os.path.join(screen_dir, "mod2_01_menu_banve.png"), "Hình 4.4: Màn hình bán vé tại quầy POS ban đầu")

    doc.add_paragraph("• Bước 2: Nhân viên hỏi tên phim khách muốn xem và nhập từ khóa tìm kiếm (Ví dụ: 'Dune') -> Hệ thống lọc danh sách kết quả phim:")
    add_image_figure(doc, os.path.join(screen_dir, "mod2_02_tim_va_chon_phim.png"), "Hình 4.5: Tìm kiếm phim theo tên và lọc kết quả danh mục phim")

    doc.add_paragraph("• Bước 3 & 4: Nhân viên chọn phim -> Hệ thống hiển thị các khung giờ xem trong ngày. Nhân viên click chọn suất chiếu (16:00 - Cinema Hall 01 IMAX):")
    add_image_figure(doc, os.path.join(screen_dir, "mod2_03_chon_gio_xem.png"), "Hình 4.6: Chọn phim và hiển thị danh sách các suất chiếu trong ngày")

    doc.add_paragraph("• Bước 5: Hệ thống hiển thị sơ đồ phòng chiếu với trạng thái từng ghế. Nhân viên chọn các vị trí ghế ngồi theo yêu cầu của khách (Chọn ghế VIP D04, D05):")
    add_image_figure(doc, os.path.join(screen_dir, "mod2_04_chon_ghe.png"), "Hình 4.7: Sơ đồ phòng chiếu trực quan và chọn ghế ngồi (VIP D04, D05)")

    doc.add_paragraph("• Bước 6: Nhân viên hỏi và nhập mã thẻ khách hàng thân thiết (MB-8888) -> Hệ thống tự động áp dụng chiết khấu giảm giá 15% VIP (-39,000 đ) và tính điểm thưởng (+22 pts):")
    add_image_figure(doc, os.path.join(screen_dir, "mod2_05_nhap_the_thanh_vien.png"), "Hình 4.8: Nhập mã thẻ thành viên, tự động chiết khấu giảm giá và tính điểm thưởng")

    doc.add_paragraph("• Bước 7 & 8: Nhân viên chọn phương thức thanh toán, click 'Xác nhận mua vé' -> Hệ thống thực thi giao dịch CSDL và in vé xem phim kèm hóa đơn bán lẻ:")
    add_image_figure(doc, os.path.join(screen_dir, "mod2_06_in_ve_hoa_don.png"), "Hình 4.9: Mẫu in Hóa đơn thanh toán bán vé và các cuống vé xem phim giao cho khách")

    doc.add_page_break()

    # ==================== PHẦN E: PHỤ LỤC PROMPT ====================
    add_heading_with_spacing(doc, "PHẦN E: PHỤ LỤC CÁC PROMPT ĐÃ DÙNG VÀ MÔ TẢ CÁCH SỬ DỤNG AI", level=1)
    doc.add_paragraph(
        "Nhằm tuân thủ nghiêm túc quy chế học vụ của Học viện và yêu cầu của giảng viên ĐỖ THỊ BÍCH NGỌC: "
        "\"Phụ lục các prompt đã dùng và mô tả rõ em sử dụng kết quả của prompt như nào (dùng luôn, edit, tham khảo và vẽ lại...); "
        "copy bài khác, dùng AI còn nhiều lỗi cơ bản => 0 điểm\", "
        "bảng dưới đây giải trình trung thực toàn bộ các câu prompt đã sử dụng và quy trình sinh viên tự rà soát, phát hiện và sửa các lỗi sai do AI tạo ra:"
    )

    tbl_pr = doc.add_table(rows=1, cols=4)
    tbl_pr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pr)
    h_pr = tbl_pr.rows[0].cells
    for i, t in enumerate(["STT", "Mục tiêu & Giai đoạn", "Câu Prompt đã dùng", "Cách sinh viên sử dụng & Sửa lỗi do AI sinh ra"]):
        h_pr[i].paragraphs[0].add_run(t).bold = True
        set_cell_background(h_pr[i], "E2E8F0")

    pr_rows = [
        ("1", "Đặc tả yêu cầu:\nKhảo sát quy trình nghiệp vụ",
         "\"Hãy liệt kê các bước trong quy trình bán vé tại quầy của rạp chiếu phim hiện đại (CGV/Lotte), có bước kiểm tra thẻ khách hàng thành viên và in vé.\"",
         "• Cách SV sử dụng: Tham khảo các bước thực tế của rạp phim lớn, sau đó đối chiếu với đề bài của cô Đặng Thị Bích Ngọc. SV loại bỏ các bước rườm rà (như gợi ý bắp nước) để bám sát đúng 2 chức năng đề bài yêu cầu: Đăng ký thành viên và Bán vé tại quầy."),
        ("2", "Đặc tả yêu cầu:\nSinh mã PlantUML Use Case",
         "\"Viết code PlantUML cho sơ đồ Use Case tổng quát hệ thống rạp chiếu phim CineMan với 3 tác nhân: Khách hàng, Nhân viên bán hàng, Nhân viên quản lý, có hậu tố 108 theo mã sinh viên B23DCCN108.\"",
         "• Cách SV sử dụng: AI ban đầu sinh sai: gắn quan hệ <<include>> cho chức năng nhập thẻ thành viên. SV đã tự rà soát và vẽ lại bằng PlantUML: chuyển bước thẻ thành viên sang <<extend>> vì đề bài ghi rõ 'nếu có'. Bổ sung đầy đủ hậu tố 108 cho mọi ca sử dụng."),
        ("3", "Phân tích hệ thống:\nBiểu đồ lớp BCE",
         "\"Tạo mã PlantUML biểu đồ lớp phân tích theo phương pháp BCE (Boundary - Control - Entity) cho hệ thống CineMan rạp chiếu phim.\"",
         "• Cách SV sử dụng: Sinh viên kiểm tra thấy AI thiếu lớp thực thể TheThanhVien108 và chưa tách lớp trừu tượng NguoiDung108. SV đã tự bổ sung đầy đủ các thuộc tính, quan hệ 1-1 giữa KhachHang108 và TheThanhVien108, quan hệ 1-N giữa HoaDon108 và Ve108."),
        ("4", "Thiết kế hệ thống:\nBiểu đồ tuần tự thiết kế",
         "\"Sinh biểu đồ trình tự thiết kế chi tiết cho ca sử dụng Bán vé tại quầy theo kiến trúc 3 lớp MVC có các lớp DAO và Transaction Database.\"",
         "• Cách SV sử dụng: SV tham khảo luồng tương tác, sau đó tự chuẩn hóa lại toàn bộ tên hàm theo chuẩn Java camelCase đồng nhất với Design Class Diagram (timKiemPhim, layTrangThaiGhe, tinhChietKhau, taoHoaDon, taoVe). Thêm cơ chế Transaction rollback khi có lỗi."),
        ("5", "Lập trình & Demo:\nKhung ứng dụng web Flask",
         "\"Gợi ý khung ứng dụng web Python Flask theo mô hình 3 lớp MVC, có cơ sở dữ liệu SQLite và sơ đồ ghế rạp chiếu phim.\"",
         "• Cách SV sử dụng: SV chỉ lấy ý tưởng cấu trúc thư mục làm sườn; tự viết toàn bộ các file DAO với câu truy vấn SQL chuẩn khóa ngoại; tự lập trình thuật toán tính chiết khấu giảm giá theo hạng thẻ (VIP 15%, Gold 10%, Silver 7%, Standard 5%) và tích điểm tự động 10%.")
    ]
    for r_d in pr_rows:
        row = tbl_pr.add_row()
        for i, val in enumerate(r_d):
            c = row.cells[i]
            c.paragraphs[0].add_run(val)
            set_cell_margins(c)

    add_heading_with_spacing(doc, "PHẦN F: BẢNG TỰ ĐÁNH GIÁ (KHIÊM TỐN, CHÂN THỰC: 8.25 / 10.0)", level=1)
    doc.add_paragraph(
        "Căn cứ vào biểu mẫu tự đánh giá trực tuyến của bộ môn (https://forms.gle/yuLGeZZtWheGsnPu5), "
        "sinh viên Hoàng Mạnh Cường (B23DCCN108) nghiêm túc tự đánh giá kết quả thực hiện đồ án CineMan theo tinh thần khiêm tốn, trung thực, "
        "không tự chấm điểm tối đa 10/10 mà thẳng thắn nhìn nhận các điểm đạt được và các hạn chế kỹ thuật còn tồn đọng:"
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
         "Đã xây dựng Bảng từ khóa 3 nhóm, bảng ngữ nghĩa 24 khái niệm, mô tả luồng --->, Use Case tổng quan & chi tiết có hậu tố 108 chuẩn form mẫu bài giảng PTIT.",
         "Chưa đặc tả sâu các ca sử dụng ngoại lệ phức tạp như khách hàng đổi vé hoặc sự cố kỹ thuật phòng chiếu.",
         "1.75 / 2.0"),
        ("2. Phân tích hệ thống\n(Thang điểm 2.0)",
         "Trích thực thể theo quy trình 5 bước; Biểu đồ lớp thực thể 108 rõ ràng; Kịch bản v1, v2; Đầy đủ Biểu đồ giao tiếp (Communication) và Trình tự phân tích cho cả 2 module.",
         "Một số thông điệp trong biểu đồ giao tiếp còn viết gộp, chưa phân tách tối đa các bước rẽ nhánh ngoại lệ nhỏ.",
         "1.75 / 2.0"),
        ("3. Thiết kế hệ thống\n(Thang điểm 2.5)",
         "Kiến trúc MVC phân tầng kết hợp DAO; ERD chuẩn 3NF và từ điển 9 bảng CSDL; Design Class Diagram có đầy đủ kiểu dữ liệu, phương thức (+/-); Biểu đồ hoạt động và Biểu đồ tuần tự thiết kế có chi tiết DAO; Biểu đồ gói & triển khai đầy đủ.",
         "Biểu đồ lớp thiết kế mới tập trung vào các lớp nghiệp vụ của 2 chức năng chính, các chức năng quản trị phim/phòng chiếu chưa chi tiết hóa hết phương thức DAO.",
         "2.0 / 2.5"),
        ("4. Lập trình và Demo\n(Thang điểm 2.5)",
         "Ứng dụng web Python Flask chạy thực tế mượt mà; Demo xuất sắc và rõ ràng 2 module của đề bài (Đăng ký thành viên và Bán vé tại quầy); Sơ đồ ghế trực quan; In vé và hóa đơn chi tiết; Lưu dữ liệu thật trong SQLite; Đã push GitHub và share quyền cho dtbnptit@gmail.com.",
         "Chưa tích hợp cổng thanh toán trực tuyến bên thứ 3 thực tế (VNPay / MoMo) mà mới thực hiện mô phỏng quy trình thanh toán; chưa kết nối máy in nhiệt chuyên dụng tại quầy.",
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

    # Đảm bảo 100% màu chữ trong toàn bộ văn bản (đoạn văn, tiêu đề, bảng biểu) là màu đen mặc định
    for p in doc.paragraphs:
        for r in p.runs:
            r.font.color.rgb = RGBColor(0, 0, 0)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.color.rgb = RGBColor(0, 0, 0)

    doc.save(out_docx)
    try:
        shutil.copyfile(out_docx, out_docx_d22)
    except PermissionError:
        pass
    print(f"[OK] Đã xuất file báo cáo hoàn chỉnh thành công:\n -> {out_docx} ({os.path.getsize(out_docx)} bytes)")

if __name__ == '__main__':
    build_report()
