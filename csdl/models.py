from django.db import models

# Người dùng
class NguoiDung(models.Model):
    MaNguoiDung = models.AutoField(primary_key=True)
    HoTen = models.CharField(max_length=255)
    SDT = models.CharField(max_length=15)
    NgaySinh = models.DateField()
    GioiTinh = models.CharField(max_length=10)
    ChucVu = models.CharField(max_length=100)

    def __str__(self):
        return self.HoTen


# Tài khoản
class TaiKhoan(models.Model):
    MaTK = models.AutoField(primary_key=True)
    TenDangNhap = models.CharField(max_length=255)
    MatKhau = models.CharField(max_length=255)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return self.TenDangNhap


# Danh mục
class DanhMuc(models.Model):
    MaDM = models.AutoField(primary_key=True)
    TenDM = models.CharField(max_length=255)

    def __str__(self):
        return self.TenDM


# Bài viết
class BaiViet(models.Model):
    MaBV = models.AutoField(primary_key=True)
    TieuDe = models.CharField(max_length=255)
    ThoiGianDang = models.DateTimeField()
    NoiDung = models.TextField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    MaDM = models.ForeignKey(DanhMuc, on_delete=models.CASCADE)

    def __str__(self):
        return self.TieuDe


# Duyệt bài viết
class DuyetBaiViet(models.Model):
    MaDuyet = models.AutoField(primary_key=True)
    NgayDuyet = models.DateTimeField()
    TrangThai = models.BooleanField()
    GhiChu = models.TextField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return f"Duyệt bài {self.MaDuyet}"


# Lịch đăng bài
class LichDangBai(models.Model):
    MaLDB = models.AutoField(primary_key=True)
    ThoiGianDang = models.DateTimeField()
    TrangThai = models.BooleanField()
    MaBV = models.ForeignKey(BaiViet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lịch đăng bài {self.MaLDB}"


# Thẻ
class The(models.Model):
    MaThe = models.AutoField(primary_key=True)
    TenThe = models.CharField(max_length=255)
    Slug = models.SlugField(unique=True)

    def __str__(self):
        return self.TenThe


# Bài viết Thẻ
class BaiVietThe(models.Model):
    MaThe = models.ForeignKey(The, on_delete=models.CASCADE)
    MaBV = models.ForeignKey(BaiViet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bài viết thẻ {self.MaThe} - {self.MaBV}"
