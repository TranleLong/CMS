from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from csdl.models import NguoiDung, TaiKhoan, DanhMuc, BaiViet, DuyetBaiViet, LichDangBai, The, BaiVietThe
def add_sample_data(request):
    # Thêm dữ liệu vào bảng NguoiDung
    NguoiDung.objects.create(HoTen="Nguyễn A", SDT="0912345678", NgaySinh="1990-05-01", GioiTinh="Nam", ChucVu="Quản lý")
    NguoiDung.objects.create(HoTen="Trần B", SDT="0987654321", NgaySinh="1985-11-22", GioiTinh="Nữ", ChucVu="Nhân viên")
    NguoiDung.objects.create(HoTen="Lê C", SDT="0911122334", NgaySinh="1992-02-15", GioiTinh="Nam", ChucVu="Giám đốc")

    # Thêm dữ liệu vào bảng TaiKhoan
    TaiKhoan.objects.create(TenDangNhap="admin", MatKhau="123456", MaNguoiDung=NguoiDung.objects.get(HoTen="Nguyễn A"))
    TaiKhoan.objects.create(TenDangNhap="user_01", MatKhau="abcdef", MaNguoiDung=NguoiDung.objects.get(HoTen="Trần B"))
    TaiKhoan.objects.create(TenDangNhap="manager", MatKhau="qwerty", MaNguoiDung=NguoiDung.objects.get(HoTen="Lê C"))

    # Thêm dữ liệu vào bảng DanhMuc
    DanhMuc.objects.create(TenDM="Công nghệ")
    DanhMuc.objects.create(TenDM="Kinh doanh")
    DanhMuc.objects.create(TenDM="Giải trí")

    # Thêm dữ liệu vào bảng BaiViet
    BaiViet.objects.create(TieuDe="Công nghệ mới", ThoiGianDang="2025-04-08 14:00:00", NoiDung="Đây là nội dung bài viết về công nghệ", MaNguoiDung=NguoiDung.objects.get(HoTen="Nguyễn A"), MaDM=DanhMuc.objects.get(TenDM="Công nghệ"))
    BaiViet.objects.create(TieuDe="Kinh doanh hiện đại", ThoiGianDang="2025-04-08 15:00:00", NoiDung="Đây là nội dung bài viết về kinh doanh", MaNguoiDung=NguoiDung.objects.get(HoTen="Trần B"), MaDM=DanhMuc.objects.get(TenDM="Kinh doanh"))
    BaiViet.objects.create(TieuDe="Giải trí thú vị", ThoiGianDang="2025-04-08 16:00:00", NoiDung="Đây là nội dung bài viết về giải trí", MaNguoiDung=NguoiDung.objects.get(HoTen="Lê C"), MaDM=DanhMuc.objects.get(TenDM="Giải trí"))

    # Thêm dữ liệu vào bảng DuyetBaiViet
    DuyetBaiViet.objects.create(NgayDuyet="2025-04-08 17:00:00", TrangThai=True, GhiChu="Bài viết được duyệt", MaNguoiDung=NguoiDung.objects.get(HoTen="Nguyễn A"))
    DuyetBaiViet.objects.create(NgayDuyet="2025-04-08 18:00:00", TrangThai=True, GhiChu="Bài viết được duyệt", MaNguoiDung=NguoiDung.objects.get(HoTen="Trần B"))
    DuyetBaiViet.objects.create(NgayDuyet="2025-04-08 19:00:00", TrangThai=False, GhiChu="Bài viết bị từ chối", MaNguoiDung=NguoiDung.objects.get(HoTen="Lê C"))

    # Thêm dữ liệu vào bảng LichDangBai
    LichDangBai.objects.create(ThoiGianDang="2025-04-08 20:00:00", TrangThai=True, MaBV=BaiViet.objects.get(TieuDe="Công nghệ mới"))
    LichDangBai.objects.create(ThoiGianDang="2025-04-08 21:00:00", TrangThai=True, MaBV=BaiViet.objects.get(TieuDe="Kinh doanh hiện đại"))
    LichDangBai.objects.create(ThoiGianDang="2025-04-08 22:00:00", TrangThai=False, MaBV=BaiViet.objects.get(TieuDe="Giải trí thú vị"))

    # Thêm dữ liệu vào bảng The
    The.objects.create(TenThe="Tin tức", Slug="tin-tuc")
    The.objects.create(TenThe="Chính trị", Slug="chinh-tri")
    The.objects.create(TenThe="Xã hội", Slug="xa-hoi")

    # Thêm dữ liệu vào bảng BaiVietThe
    BaiVietThe.objects.create(MaThe=The.objects.get(TenThe="Tin tức"), MaBV=BaiViet.objects.get(TieuDe="Công nghệ mới"))
    BaiVietThe.objects.create(MaThe=The.objects.get(TenThe="Chính trị"), MaBV=BaiViet.objects.get(TieuDe="Kinh doanh hiện đại"))
    BaiVietThe.objects.create(MaThe=The.objects.get(TenThe="Xã hội"), MaBV=BaiViet.objects.get(TieuDe="Giải trí thú vị"))

    # Trả về một template hoặc một phản hồi
    return render(request, 'index.html')

def get_content(request, target):
    if target == 'baiviet':
        # Trả về nội dung block bài viết
        context = {
            'baiviet_data': 'Nội dung bài viết mặc định'
        }
        return render(request, 'quanlybaiviet.html', context)
    elif target == 'danhmuc':
        # Trả về nội dung block danh mục
        context = {
            'danhmuc_data': 'Nội dung danh mục'
        }
        return render(request, 'content/partial/danhmuc.html', context)
    else:
        # Trả về nội dung mặc định cho trang chủ
        return render(request, 'content/partial/home.html')
