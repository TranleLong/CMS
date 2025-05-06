# from django.shortcuts import render
#
# # Create your views here.
# from django.shortcuts import render
# from csdl.models import NguoiDung, TaiKhoan, DanhMuc, BaiViet, DuyetBaiViet, LichDangBai, The, BaiVietThe
# def add_sample_data(request):
#     # Thêm dữ liệu vào bảng NguoiDung
#     NguoiDung.objects.create(HoTen="Nguyễn A", SDT="0912345678", NgaySinh="1990-05-01", GioiTinh="Nam", ChucVu="Quản lý")
#     NguoiDung.objects.create(HoTen="Trần B", SDT="0987654321", NgaySinh="1985-11-22", GioiTinh="Nữ", ChucVu="Nhân viên")
#     NguoiDung.objects.create(HoTen="Lê C", SDT="0911122334", NgaySinh="1992-02-15", GioiTinh="Nam", ChucVu="Giám đốc")
#
#     # Thêm dữ liệu vào bảng TaiKhoan
#     TaiKhoan.objects.create(TenDangNhap="admin", MatKhau="123456", MaNguoiDung=NguoiDung.objects.get(HoTen="Nguyễn A"))
#     TaiKhoan.objects.create(TenDangNhap="user_01", MatKhau="abcdef", MaNguoiDung=NguoiDung.objects.get(HoTen="Trần B"))
#     TaiKhoan.objects.create(TenDangNhap="manager", MatKhau="qwerty", MaNguoiDung=NguoiDung.objects.get(HoTen="Lê C"))
#
#     # Thêm dữ liệu vào bảng DanhMuc
#     DanhMuc.objects.create(TenDM="Công nghệ")
#     DanhMuc.objects.create(TenDM="Kinh doanh")
#     DanhMuc.objects.create(TenDM="Giải trí")
#
#     # Thêm dữ liệu vào bảng BaiViet
#     BaiViet.objects.create(TieuDe="Công nghệ mới", ThoiGianDang="2025-04-08 14:00:00", NoiDung="Đây là nội dung bài viết về công nghệ", MaNguoiDung=NguoiDung.objects.get(HoTen="Nguyễn A"), MaDM=DanhMuc.objects.get(TenDM="Công nghệ"))
#     BaiViet.objects.create(TieuDe="Kinh doanh hiện đại", ThoiGianDang="2025-04-08 15:00:00", NoiDung="Đây là nội dung bài viết về kinh doanh", MaNguoiDung=NguoiDung.objects.get(HoTen="Trần B"), MaDM=DanhMuc.objects.get(TenDM="Kinh doanh"))
#     BaiViet.objects.create(TieuDe="Giải trí thú vị", ThoiGianDang="2025-04-08 16:00:00", NoiDung="Đây là nội dung bài viết về giải trí", MaNguoiDung=NguoiDung.objects.get(HoTen="Lê C"), MaDM=DanhMuc.objects.get(TenDM="Giải trí"))
#
#     # Thêm dữ liệu vào bảng DuyetBaiViet
#     DuyetBaiViet.objects.create(NgayDuyet="2025-04-08 17:00:00", TrangThai=True, GhiChu="Bài viết được duyệt", MaNguoiDung=NguoiDung.objects.get(HoTen="Nguyễn A"))
#     DuyetBaiViet.objects.create(NgayDuyet="2025-04-08 18:00:00", TrangThai=True, GhiChu="Bài viết được duyệt", MaNguoiDung=NguoiDung.objects.get(HoTen="Trần B"))
#     DuyetBaiViet.objects.create(NgayDuyet="2025-04-08 19:00:00", TrangThai=False, GhiChu="Bài viết bị từ chối", MaNguoiDung=NguoiDung.objects.get(HoTen="Lê C"))
#
#     # Thêm dữ liệu vào bảng LichDangBai
#     LichDangBai.objects.create(ThoiGianDang="2025-04-08 20:00:00", TrangThai=True, MaBV=BaiViet.objects.get(TieuDe="Công nghệ mới"))
#     LichDangBai.objects.create(ThoiGianDang="2025-04-08 21:00:00", TrangThai=True, MaBV=BaiViet.objects.get(TieuDe="Kinh doanh hiện đại"))
#     LichDangBai.objects.create(ThoiGianDang="2025-04-08 22:00:00", TrangThai=False, MaBV=BaiViet.objects.get(TieuDe="Giải trí thú vị"))
#
#     # Thêm dữ liệu vào bảng The
#     The.objects.create(TenThe="Tin tức", Slug="tin-tuc")
#     The.objects.create(TenThe="Chính trị", Slug="chinh-tri")
#     The.objects.create(TenThe="Xã hội", Slug="xa-hoi")
#
#     # Thêm dữ liệu vào bảng BaiVietThe
#     BaiVietThe.objects.create(MaThe=The.objects.get(TenThe="Tin tức"), MaBV=BaiViet.objects.get(TieuDe="Công nghệ mới"))
#     BaiVietThe.objects.create(MaThe=The.objects.get(TenThe="Chính trị"), MaBV=BaiViet.objects.get(TieuDe="Kinh doanh hiện đại"))
#     BaiVietThe.objects.create(MaThe=The.objects.get(TenThe="Xã hội"), MaBV=BaiViet.objects.get(TieuDe="Giải trí thú vị"))
#
#     # Trả về một template hoặc một phản hồi
#     return render(request, 'index.html')
#
# def get_content(request, target):
#     if target == 'baiviet':
#         # Trả về nội dung block bài viết
#         context = {
#             'baiviet_data': 'Nội dung bài viết mặc định'
#         }
#         return render(request, 'quanlybaiviet.html', context)
#     elif target == 'danhmuc':
#         # Trả về nội dung block danh mục
#         context = {
#             'danhmuc_data': 'Nội dung danh mục'
#         }
#         return render(request, 'content/partial/danhmuc.html', context)
#     else:
#         # Trả về nội dung mặc định cho trang chủ
#         return render(request, 'content/partial/home.html')
from django.shortcuts import render
from django.contrib.auth.models import User
from csdl.models import DanhMuc, BaiViet, DuyetBaiViet, LichDangBai, The, BaiVietThe, Media
from django.utils import timezone  # Import timezone

def add_sample_data(request):
    # Thêm dữ liệu vào bảng User (auth_user)
    user1 = User.objects.create_user(username="nguyena", password="123456", first_name="Nguyễn", last_name="A", email="nguyena@example.com", last_login=timezone.now())
    user2 = User.objects.create_user(username="tranb", password="abcdef", first_name="Trần", last_name="B", email="tranb@example.com", last_login=timezone.now())
    user3 = User.objects.create_user(username="lec", password="qwerty", first_name="Lê", last_name="C", email="lec@example.com", last_login=timezone.now())

    # Thêm dữ liệu vào bảng DanhMuc
    danh_muc1 = DanhMuc.objects.create(
        ten_dm="Công nghệ", slug="cong-nghe", so_bai_viet=0, parent_id=None, order_index=1, mo_ta="Mô tả về công nghệ",
        trang_thai=True
    )
    danh_muc2 = DanhMuc.objects.create(
        ten_dm="Kinh doanh", slug="kinh-doanh", so_bai_viet=0, parent_id=None, order_index=2,
        mo_ta="Mô tả về kinh doanh", trang_thai=True
    )
    danh_muc3 = DanhMuc.objects.create(
        ten_dm="Giải trí", slug="giai-tri", so_bai_viet=0, parent_id=None, order_index=3, mo_ta="Mô tả về giải trí",
        trang_thai=False
    )

    # Thêm dữ liệu vào bảng The
    the1 = The.objects.create(ten_the="Tin tức", slug="tin-tuc", so_bai_viet=10, mo_ta="Các bài viết tin tức")
    the2 = The.objects.create(ten_the="Chính trị", slug="chinh-tri", so_bai_viet=5, mo_ta="Các bài viết chính trị")
    the3 = The.objects.create(ten_the="Xã hội", slug="xa-hoi", so_bai_viet=8, mo_ta="Các bài viết xã hội")

    # Sau khi tạo các thẻ, sử dụng chúng trong các bài viết
    bai_viet1 = BaiViet.objects.create(
        tieu_de="Công nghệ mới", ngay_dang=timezone.now(), noi_dung="Đây là nội dung bài viết về công nghệ",
        duong_dan="http://example.com/bai-viet-1", tom_tat="Bài viết về công nghệ", ma_nguoi_dung=user1,
        ma_dm=danh_muc1, ma_the=the1
    )
    bai_viet2 = BaiViet.objects.create(
        tieu_de="Kinh doanh hiện đại", ngay_dang=timezone.now(), noi_dung="Đây là nội dung bài viết về kinh doanh",
        duong_dan="http://example.com/bai-viet-2", tom_tat="Bài viết về kinh doanh", ma_nguoi_dung=user2,
        ma_dm=danh_muc2, ma_the=the2
    )
    bai_viet3 = BaiViet.objects.create(
        tieu_de="Giải trí thú vị", ngay_dang=timezone.now(), noi_dung="Đây là nội dung bài viết về giải trí",
        duong_dan="http://example.com/bai-viet-3", tom_tat="Bài viết về giải trí", ma_nguoi_dung=user3, ma_dm=danh_muc3,
        ma_the=the3
    )

    # Thêm dữ liệu vào bảng DuyetBaiViet
    DuyetBaiViet.objects.create(ngay_duyet=timezone.now(), trang_thai="Đã duyệt", ghi_chu="Bài viết được duyệt", ma_nguoi_dung=user1, ma_bai_viet=bai_viet1)
    DuyetBaiViet.objects.create(ngay_duyet=timezone.now(), trang_thai="Đã duyệt", ghi_chu="Bài viết được duyệt", ma_nguoi_dung=user2, ma_bai_viet=bai_viet2)
    DuyetBaiViet.objects.create(ngay_duyet=timezone.now(), trang_thai="Bị từ chối", ghi_chu="Bài viết bị từ chối", ma_nguoi_dung=user3, ma_bai_viet=bai_viet3)

    # Thêm dữ liệu vào bảng LichDangBai
    LichDangBai.objects.create(ngay_dang=timezone.now(), do_uu_tien=True, ngay_dong=None, ma_bv=bai_viet1, ma_nguoi_dung=user1)
    LichDangBai.objects.create(ngay_dang=timezone.now(), do_uu_tien=False, ngay_dong=None, ma_bv=bai_viet2, ma_nguoi_dung=user2)
    LichDangBai.objects.create(ngay_dang=timezone.now(), do_uu_tien=False, ngay_dong=None, ma_bv=bai_viet3, ma_nguoi_dung=user3)

    # Thêm dữ liệu vào bảng The


    # Thêm dữ liệu vào bảng BaiVietThe
    BaiVietThe.objects.create(ma_the=the1, ma_bv=bai_viet1)
    BaiVietThe.objects.create(ma_the=the2, ma_bv=bai_viet2)
    BaiVietThe.objects.create(ma_the=the3, ma_bv=bai_viet3)

    # Thêm dữ liệu vào bảng Media
    media1 = Media.objects.create(folder_name="images", file_name="image1.jpg", type_name="jpg", size=500, ma_nguoi_dung=user1)
    media2 = Media.objects.create(folder_name="videos", file_name="video1.mp4", type_name="mp4", size=1500, ma_nguoi_dung=user2)
    media3 = Media.objects.create(folder_name="documents", file_name="doc1.pdf", type_name="pdf", size=300, ma_nguoi_dung=user3)

    # Trả về một template hoặc một phản hồi
    return render(request, 'index.html')
