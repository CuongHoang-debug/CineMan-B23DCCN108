import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime

# Import Controllers
from controllers.auth_controller import AuthController
from controllers.khach_hang_controller import KhachHangController
from controllers.ban_ve_controller import BanVeController
from controllers.phim_controller import PhimController
from controllers.thong_ke_controller import ThongKeController

app = Flask(__name__)
app.secret_key = 'cineman_ptit_secret_key_2026'

auth_ctrl = AuthController()
kh_ctrl = KhachHangController()
ban_ve_ctrl = BanVeController()
phim_ctrl = PhimController()
thong_ke_ctrl = ThongKeController()

@app.context_processor
def inject_user():
    return {
        'current_user': session.get('user'),
        'now_year': datetime.now().year
    }

@app.route('/dev-login/<role>')
@app.route('/dev-login/<role>/<target>')
def dev_login(role, target=''):
    if role == 'BAN_HANG':
        session['user'] = {'id': 2, 'taiKhoan': 'staff', 'hoTen': 'Nguyễn Thu Ngân', 'sdt': '0923456789', 'email': 'staff@cineman.vn', 'vaiTro': 'BAN_HANG'}
        return redirect(url_for('staff_pos', **request.args))
    elif role == 'QUAN_LY':
        session['user'] = {'id': 1, 'taiKhoan': 'admin', 'hoTen': 'Trần Đức Quản Lý', 'sdt': '0912345678', 'email': 'admin@cineman.vn', 'vaiTro': 'QUAN_LY'}
        if target == 'movies':
            return redirect(url_for('manager_movies'))
        elif target == 'schedules':
            return redirect(url_for('manager_schedules'))
        elif target == 'customers':
            return redirect(url_for('manager_customers'))
        return redirect(url_for('manager_dashboard'))
    return redirect(url_for('login'))

# ----------------- AUTHENTICATION -----------------
@app.route('/')
def index():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    if user['vaiTro'] == 'QUAN_LY':
        return redirect(url_for('manager_dashboard'))
    elif user['vaiTro'] == 'BAN_HANG':
        return redirect(url_for('staff_pos'))
    else:
        return redirect(url_for('customer_home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tai_khoan = request.form.get('taiKhoan', '')
        mat_khau = request.form.get('matKhau', '')
        user = auth_ctrl.dang_nhap(tai_khoan, mat_khau)
        if user:
            session['user'] = user
            flash(f"Xin chào {user['hoTen']}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không chính xác!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Bạn đã đăng xuất thành công.", "info")
    return redirect(url_for('login'))

# ----------------- KHÁCH HÀNG: ĐĂNG KÝ THÀNH VIÊN -----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ho_ten = request.form.get('hoTen', '')
        sdt = request.form.get('sdt', '')
        email = request.form.get('email', '')
        cccd = request.form.get('cccd', '')
        mat_khau = request.form.get('matKhau', '')
        ngay_sinh = request.form.get('ngaySinh', '')
        dia_chi = request.form.get('diaChi', '')

        result = kh_ctrl.dang_ky_thanh_vien(ho_ten, sdt, email, cccd, mat_khau, ngay_sinh, dia_chi)
        if result['success']:
            flash(result['message'], "success")
            return render_template('register_success.html', data=result['data'])
        else:
            flash(result['message'], "danger")
    return render_template('register.html')

@app.route('/demo/register-filled')
def demo_register_filled():
    return render_template('demo_register_filled.html')

@app.route('/demo/register-success')
def demo_register_success():
    sample_data = {
        'ho_ten': 'Nguyễn Tuấn Anh',
        'ma_the': 'MB-2026',
        'hang_the': 'Standard',
        'diem': 0,
        'sdt': '0988123456'
    }
    return render_template('register_success.html', data=sample_data)

@app.route('/demo/sqlite-view')
def demo_sqlite_view():
    from dao.db_connection import DBConnection
    conn = DBConnection.get_instance().get_connection()
    c = conn.cursor()
    c.execute('''
    SELECT u.id, u.hoTen, u.sdt, u.email, k.cccd, k.ngaySinh, t.maThe, t.hangThe, t.diemTichLuy
    FROM tblNguoiDung u
    JOIN tblKhachHang k ON u.id = k.id
    LEFT JOIN tblTheThanhVien t ON k.id = t.idKhachHang
    ORDER BY u.id DESC
    ''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return render_template('demo_sqlite_view.html', rows=rows)

@app.route('/customer/home')
def customer_home():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    movies = phim_ctrl.lay_danh_sach()
    # Tim thong tin the cua user neu co
    the_info = None
    if user['vaiTro'] == 'KHACH_HANG':
        kh_list = kh_ctrl.lay_danh_sach()
        for k in kh_list:
            if k['id'] == user['id']:
                the_info = k
                break
    return render_template('customer_home.html', movies=movies, the_info=the_info)

# ----------------- NHÂN VIÊN: BÁN VÉ TẠI QUẦY (POS) -----------------
@app.route('/pos')
def staff_pos():
    user = session.get('user')
    if not user or user['vaiTro'] not in ['BAN_HANG', 'QUAN_LY']:
        flash("Bạn không có quyền truy cập khu vực Bán vé!", "warning")
        return redirect(url_for('login'))
    movies = phim_ctrl.lay_danh_sach()
    return render_template('staff_pos.html', movies=movies)

# APIs cho màn hình POS bán vé
@app.route('/api/movies/search')
def api_search_movies():
    kw = request.args.get('keyword', '')
    movies = ban_ve_ctrl.tim_kiem_phim(kw)
    return jsonify(movies)

@app.route('/api/movies/<int:movie_id>/showtimes')
def api_movie_showtimes(movie_id):
    date_filter = request.args.get('date', None)
    data = ban_ve_ctrl.chon_phim(movie_id, date_filter)
    return jsonify(data)

@app.route('/api/showtimes/<int:schedule_id>/seats')
def api_showtime_seats(schedule_id):
    data = ban_ve_ctrl.chon_suat_chieu(schedule_id)
    return jsonify(data)

@app.route('/api/members/<card_code>')
def api_lookup_member(card_code):
    member = kh_ctrl.tra_cuu_the(card_code)
    if member:
        return jsonify({"found": True, "member": member})
    return jsonify({"found": False, "message": "Không tìm thấy thẻ thành viên này!"})

@app.route('/api/calculate-price', methods=['POST'])
def api_calculate_price():
    payload = request.json or {}
    schedule_id = payload.get('schedule_id')
    seat_ids = payload.get('seat_ids', [])
    card_code = payload.get('card_code', '')
    calc = ban_ve_ctrl.tinh_tien(schedule_id, seat_ids, card_code)
    return jsonify(calc)

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    user = session.get('user')
    if not user:
        return jsonify({"success": False, "message": "Phiên làm việc đã hết hạn!"}), 401
    payload = request.json or {}
    schedule_id = payload.get('schedule_id')
    seat_ids = payload.get('seat_ids', [])
    card_code = payload.get('card_code', '')
    payment_method = payload.get('payment_method', 'TIEN_MAT')

    res = ban_ve_ctrl.xac_nhan_thanh_toan(
        id_lich=schedule_id,
        ds_id_ghe=seat_ids,
        id_nhan_vien=user['id'],
        ma_the=card_code,
        phuong_thuc_tt=payment_method
    )
    return jsonify(res)

@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    from dao.hoa_don_dao import HoaDonDAO
    hd_dao = HoaDonDAO()
    hd = hd_dao.lay_chi_tiet(invoice_id)
    if not hd:
        flash("Không tìm thấy hóa đơn này!", "danger")
        return redirect(url_for('index'))
    return render_template('ticket_print.html', hd=hd)

# ----------------- QUẢN LÝ: DASHBOARD, PHIM, PHÒNG, LỊCH CHIẾU -----------------
@app.route('/manager/dashboard')
def manager_dashboard():
    user = session.get('user')
    if not user or user['vaiTro'] != 'QUAN_LY':
        flash("Bạn không có quyền truy cập trang Quản lý!", "danger")
        return redirect(url_for('login'))

    overview = thong_ke_ctrl.lay_thong_ke_tong_quan()
    movie_stats = thong_ke_ctrl.lay_thong_ke_phim()
    customer_stats = thong_ke_ctrl.lay_thong_ke_khach_hang()
    revenue_daily = thong_ke_ctrl.lay_thong_ke_doanh_thu()

    return render_template(
        'manager_dashboard.html',
        overview=overview,
        movie_stats=movie_stats,
        customer_stats=customer_stats,
        revenue_daily=revenue_daily
    )

@app.route('/manager/movies', methods=['GET', 'POST'])
def manager_movies():
    user = session.get('user')
    if not user or user['vaiTro'] != 'QUAN_LY':
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            phim_ctrl.them_phim(
                request.form.get('tenPhim'),
                request.form.get('theLoai'),
                request.form.get('thoiLuong'),
                request.form.get('daoDien'),
                request.form.get('dienVien'),
                request.form.get('doTuoi'),
                request.form.get('poster'),
                request.form.get('moTa')
            )
            flash("Thêm phim mới thành công!", "success")
        elif action == 'delete':
            movie_id = request.form.get('movie_id')
            phim_ctrl.xoa_phim(movie_id)
            flash("Đã xóa phim!", "info")

    movies = phim_ctrl.lay_danh_sach()
    return render_template('manager_movies.html', movies=movies)

@app.route('/manager/schedules', methods=['GET', 'POST'])
def manager_schedules():
    user = session.get('user')
    if not user or user['vaiTro'] != 'QUAN_LY':
        return redirect(url_for('login'))

    if request.method == 'POST':
        id_phim = request.form.get('idPhim')
        id_phong = request.form.get('idPhong')
        ngay_chieu = request.form.get('ngayChieu')
        gio_bat_dau = request.form.get('gioBatDau')
        gio_ket_thuc = request.form.get('gioKetThuc')
        gia_ve_goc = request.form.get('giaVeGoc')

        phim_ctrl.tao_lich_chieu(id_phim, id_phong, ngay_chieu, gio_bat_dau, gio_ket_thuc, gia_ve_goc)
        flash("Lên lịch chiếu thành công!", "success")

    movies = phim_ctrl.lay_danh_sach()
    rooms = phim_ctrl.lay_phong_chieu()
    schedules = phim_ctrl.lay_tat_ca_lich()
    return render_template('manager_schedules.html', movies=movies, rooms=rooms, schedules=schedules)

@app.route('/manager/customers')
def manager_customers():
    user = session.get('user')
    if not user or user['vaiTro'] != 'QUAN_LY':
        return redirect(url_for('login'))
    customers = kh_ctrl.lay_danh_sach()
    return render_template('manager_customers.html', customers=customers)

if __name__ == '__main__':
    print("=" * 60)
    print(" C I N E M A N   -   HỆ THỐNG QUẢN LÝ RẠP CHIẾU PHIM")
    print(" PTIT - Học Viện Công Nghệ Bưu Chính Viễn Thông")
    print(" Server đang chạy tại: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
