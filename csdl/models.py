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


# Bảng BaiViet
class BaiViet(models.Model):
    ma_bv = models.AutoField(primary_key=True)
    tieu_de = models.CharField(max_length=255)
    trang_thai = models.CharField(max_length=100)
    ngay_dang = models.DateField()
    duong_dan = models.URLField()
    tom_tat = models.CharField(max_length=255)
    ma_nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết trực tiếp với auth_user
    ma_dm = models.ForeignKey('DanhMuc', on_delete=models.CASCADE)
    ma_the = models.ForeignKey('The', on_delete=models.CASCADE)
    noi_dung = models.TextField()
    # Thêm trường để lưu ảnh đại diện của bài viết
    anh = models.ImageField(upload_to='images/bai_viet/', null=True, blank=True)  # Trường lưu ảnh bài viết


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
