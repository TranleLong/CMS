from django.db import models
from django.contrib.auth.models import User  # Sử dụng auth_user mặc định của Django


# Bảng DuyetBaiViet
class DuyetBaiViet(models.Model):
    ma_duyet = models.AutoField(primary_key=True)
    ngay_duyet = models.DateField()
    trang_thai = models.CharField(max_length=100)
    ghi_chu = models.TextField(null=True, blank=True)
    ma_bai_viet = models.ForeignKey('BaiViet', on_delete=models.CASCADE)
    ma_nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết trực tiếp với auth_user


# Bảng Media
class Media(models.Model):
    ma_media = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    type_name = models.CharField(max_length=50)
    size = models.IntegerField()
    # Thêm trường để lưu trữ hình ảnh hoặc file khác
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)  # Thêm trường lưu ảnh vào bảng Media
    ma_nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết trực tiếp với auth_user
# Cập nhật lại model Menu để phù hợp với menu ngang

class Menu(models.Model):
    ma_menu = models.AutoField(primary_key=True)
    tieu_de = models.CharField(max_length=255)  # Tiêu đề của menu
    slug = models.SlugField(unique=True)  # Đường dẫn của menu
    trang_thai = models.CharField(
        max_length=20,
        choices=[('Dang hoat dong', 'Đang hoạt động'), ('Khong hoat dong', 'Không hoạt động')],
        default='Dang hoat dong'
    )
    ngay_tao = models.DateField(auto_now_add=True)
    thu_tu = models.IntegerField(default=0)  # Thứ tự hiển thị của menu
    url = models.URLField(blank=True, null=True)  # Đường dẫn tùy chỉnh cho menu
    loai_menu = models.CharField(
        max_length=20,
        choices=[('bai_viet', 'Bài viết'), ('duong_dan', 'Đường dẫn')],
        default='bai_viet'
    )

    def __str__(self):
        return self.tieu_de

    class Meta:
        ordering = ['thu_tu']
        db_table = 'csdl_menu'  # Đảm bảo tên bảng đúng


class BaiViet(models.Model):
    ma_bv = models.AutoField(primary_key=True)
    tieu_de = models.CharField(max_length=255)
    trang_thai = models.CharField(max_length=100)
    ngay_dang = models.DateField()
    duong_dan = models.URLField()
    tom_tat = models.CharField(max_length=255)
    ma_nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    ma_dm = models.ForeignKey('DanhMuc', on_delete=models.CASCADE)
    ma_the = models.ForeignKey('The', on_delete=models.CASCADE)
    noi_dung = models.TextField()
    anh = models.ImageField(upload_to='images/bai_viet/', null=True, blank=True)
    # Thêm trường menu để liên kết bài viết với menu
    menu = models.ManyToManyField(Menu, through='MenuBaiViet', blank=True)

    def __str__(self):
        return self.tieu_de

    class Meta:
        db_table = 'csdl_baiviet'  # Đảm bảo tên bảng đúng


class MenuBaiViet(models.Model):
    ma_menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_bai_viet')
    ma_bv = models.ForeignKey(BaiViet, on_delete=models.CASCADE, related_name='baiviet_menu')
    thu_tu = models.IntegerField(default=0)

    class Meta:
        ordering = ['thu_tu']
        unique_together = ('ma_menu', 'ma_bv')
        db_table = 'csdl_baiviet_menu'  # Đảm bảo tên bảng đúng

# Bảng BaiVietMedia (mối quan hệ giữa bài viết và media)
class BaiVietMedia(models.Model):
    ma_bv = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    ma_media = models.ForeignKey(Media, on_delete=models.CASCADE)


# Bảng BaiVietLichDangBai (Lịch đăng bài)
class BaiVietLichDangBai(models.Model):
    ma_ldb = models.AutoField(primary_key=True)
    ma_bv = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    ma_nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết trực tiếp với auth_user


# Bảng LichDangBai (Bảng lịch đăng bài của bài viết)
class LichDangBai(models.Model):
    ma_ldb = models.AutoField(primary_key=True)
    ngay_dang = models.DateField()
    do_uu_tien = models.BooleanField(default=False)
    ngay_dong = models.DateField(null=True, blank=True)
    ma_bv = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    ma_nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết trực tiếp với auth_user


# Bảng BaiVietThe (mối quan hệ bài viết và thẻ)
class BaiVietThe(models.Model):
    ma_bv = models.ForeignKey(BaiViet, on_delete=models.CASCADE, primary_key=True)
    ma_the = models.ForeignKey('The', on_delete=models.CASCADE)


# Bảng The
class The(models.Model):
    ma_the = models.AutoField(primary_key=True)
    ten_the = models.CharField(max_length=255)
    so_bai_viet = models.IntegerField()
    slug = models.CharField(max_length=255)
    mo_ta = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.ten_the


# Bảng DanhMuc (Danh mục bài viết)
class DanhMuc(models.Model):
    ma_dm = models.AutoField(primary_key=True)
    ten_dm = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    so_bai_viet = models.IntegerField(default=0)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order_index = models.IntegerField()
    mo_ta = models.TextField(null=True, blank=True)
    trang_thai = models.BooleanField(default=True)

    def __str__(self):
        return self.ten_dm

from django.utils import timezone
class Contact(models.Model):
    TRANG_THAI_CHOICES = (
        ('moi', 'Mới'),
        ('da_xu_ly', 'Đã xử lý'),
    )

    ma_lien_he = models.AutoField(primary_key=True)
    ho_ten = models.CharField(max_length=255, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    so_dien_thoai = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    chu_de = models.CharField(max_length=100, verbose_name="Chủ đề")
    noi_dung = models.TextField(verbose_name="Nội dung")
    ngay_gui = models.DateTimeField(default=timezone.now, verbose_name="Ngày gửi")
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default='moi',
        verbose_name="Trạng thái"
    )

    class Meta:
        verbose_name = "Liên hệ"
        verbose_name_plural = "Liên hệ"
        ordering = ['-ngay_gui']

    def __str__(self):
        return f"{self.ho_ten} - {self.chu_de}"