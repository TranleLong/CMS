# from django import forms
# from csdl.models import BaiViet, DanhMuc, The
# from django.contrib.auth.models import User
# from django.utils.text import slugify
#
#
# class BaiVietForm(forms.ModelForm):
#     class Meta:
#         model = BaiViet
#         fields = ['tieu_de', 'duong_dan', 'tom_tat', 'noi_dung', 'ma_dm', 'ma_the', 'trang_thai', 'anh']
#         labels = {
#             'tieu_de': 'Tiêu đề',
#             'duong_dan': 'Đường dẫn',
#             'tom_tat': 'Tóm tắt',
#             'noi_dung': 'Nội dung',
#             'ma_dm': 'Danh mục',
#             'ma_the': 'Thẻ',
#             'trang_thai': 'Trạng thái',
#             'anh': 'Ảnh đại diện'
#         }
#         widgets = {
#             'tieu_de': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Nhập tiêu đề bài viết',
#                 'id': 'tieu_de'
#             }),
#             'duong_dan': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'nhap-duong-dan-bai-viet',
#                 'id': 'duong_dan'
#             }),
#             'tom_tat': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3,
#                 'placeholder': 'Nhập tóm tắt ngắn gọn về bài viết...',
#                 'id': 'tom_tat'
#             }),
#             'noi_dung': forms.Textarea(attrs={
#                 'class': 'form-control editor',
#                 'rows': 10,
#                 'placeholder': 'Viết nội dung bài viết ở đây...',
#                 'id': 'noi_dung'
#             }),
#             'ma_dm': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'ma_dm'
#             }),
#             'ma_the': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'ma_the'
#             }),
#             'trang_thai': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'trang_thai'
#             }, choices=[
#                 ('Chờ duyệt', 'Chờ duyệt'),
#                 ('Đăng trang', 'Đăng trang'),
#                 ('Đã duyệt', 'Đã duyệt')
#             ]),
#             'anh': forms.FileInput(attrs={
#                 'class': 'form-control',
#                 'style': 'display: none;',
#                 'accept': 'image/*',
#                 'id': 'anh'
#             })
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(BaiVietForm, self).__init__(*args, **kwargs)
#         # Đặt các trường bắt buộc
#         self.fields['tieu_de'].required = True
#         self.fields['duong_dan'].required = True
#         self.fields['noi_dung'].required = True
#         self.fields['ma_dm'].required = True
#         self.fields['ma_the'].required = True
#
#         # Các trường không bắt buộc
#         self.fields['tom_tat'].required = False
#         self.fields['anh'].required = False
#
#     def clean_duong_dan(self):
#         """Kiểm tra và chuẩn hóa đường dẫn"""
#         duong_dan = self.cleaned_data.get('duong_dan')
#         if duong_dan:
#             # Loại bỏ khoảng trắng và chuyển thành chữ thường
#             duong_dan = duong_dan.strip().lower()
#             # Thay thế khoảng trắng bằng dấu gạch ngang
#             duong_dan = duong_dan.replace(' ', '-')
#         return duong_dan
#
#     def clean(self):
#         """Kiểm tra dữ liệu form tổng thể"""
#         cleaned_data = super().clean()
#         tieu_de = cleaned_data.get('tieu_de')
#         duong_dan = cleaned_data.get('duong_dan')
#
#         # Nếu không có đường dẫn nhưng có tiêu đề, tạo đường dẫn từ tiêu đề
#         if not duong_dan and tieu_de:
#             cleaned_data['duong_dan'] = slugify(tieu_de)
#
#         return cleaned_data
#
#     def save(self, commit=True):
#         """
#         Ghi đè phương thức save để cập nhật số lượng bài viết trong danh mục và thẻ
#         """
#         instance = super(BaiVietForm, self).save(commit=False)
#
#         # Lưu instance trước để có thể truy cập các trường sau khi lưu
#         if commit:
#             # Lấy danh mục và thẻ cũ (nếu đang cập nhật bài viết)
#             old_dm = None
#             old_the = None
#
#             if instance.pk:  # Nếu đang cập nhật bài viết đã tồn tại
#                 try:
#                     old_instance = BaiViet.objects.get(pk=instance.pk)
#                     old_dm = old_instance.ma_dm
#                     old_the = old_instance.ma_the
#                 except BaiViet.DoesNotExist:
#                     pass
#
#             # Lưu instance
#             instance.save()
#
#             # Cập nhật số lượng bài viết trong danh mục và thẻ
#             self._update_count(instance, old_dm, old_the)
#
#         return instance
#
#     def _update_count(self, instance, old_dm=None, old_the=None):
#         """
#         Cập nhật số lượng bài viết trong danh mục và thẻ
#         """
#         # Cập nhật danh mục
#         if old_dm and old_dm != instance.ma_dm:
#             # Giảm số lượng bài viết trong danh mục cũ
#             old_dm.so_bai_viet = max(0, old_dm.so_bai_viet - 1)
#             old_dm.save()
#
#         # Tăng số lượng bài viết trong danh mục mới
#         if not old_dm or old_dm != instance.ma_dm:
#             instance.ma_dm.so_bai_viet += 1
#             instance.ma_dm.save()
#
#         # Cập nhật thẻ
#         if old_the and old_the != instance.ma_the:
#             # Giảm số lượng bài viết trong thẻ cũ
#             old_the.so_bai_viet = max(0, old_the.so_bai_viet - 1)
#             old_the.save()
#
#         # Tăng số lượng bài viết trong thẻ mới
#         if not old_the or old_the != instance.ma_the:
#             instance.ma_the.so_bai_viet += 1
#             instance.ma_the.save()
from django import forms
from csdl.models import BaiViet, DanhMuc, The, Menu
from django.contrib.auth.models import User
from django.utils.text import slugify


class BaiVietForm(forms.ModelForm):
    class Meta:
        model = BaiViet
        fields = ['tieu_de', 'duong_dan', 'tom_tat', 'noi_dung', 'ma_dm', 'ma_the', 'trang_thai', 'anh', 'menu']
        labels = {
            'tieu_de': 'Tiêu đề',
            'duong_dan': 'Đường dẫn',
            'tom_tat': 'Tóm tắt',
            'noi_dung': 'Nội dung',
            'ma_dm': 'Danh mục',
            'ma_the': 'Thẻ',
            'trang_thai': 'Trạng thái',
            'anh': 'Ảnh đại diện',
            'menu': 'Menu'
        }
        widgets = {
            'tieu_de': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề bài viết',
                'id': 'tieu_de'
            }),
            'duong_dan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nhap-duong-dan-bai-viet',
                'id': 'duong_dan'
            }),
            'tom_tat': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Nhập tóm tắt ngắn gọn về bài viết...',
                'id': 'tom_tat'
            }),
            'noi_dung': forms.Textarea(attrs={
                'class': 'form-control editor',
                'rows': 10,
                'placeholder': 'Viết nội dung bài viết ở đây...',
                'id': 'noi_dung'
            }),
            'ma_dm': forms.Select(attrs={
                'class': 'form-control',
                'id': 'ma_dm'
            }),
            'ma_the': forms.Select(attrs={
                'class': 'form-control',
                'id': 'ma_the'
            }),
            'menu': forms.Select(attrs={
                'class': 'form-control',
                'id': 'menu'
            }),
            'trang_thai': forms.Select(attrs={
                'class': 'form-control',
                'id': 'trang_thai'
            }, choices=[
                ('Chờ duyệt', 'Chờ duyệt'),
                ('Đăng trang', 'Đăng trang'),
                ('Đã duyệt', 'Đã duyệt')
            ]),
            'anh': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'display: none;',
                'accept': 'image/*',
                'id': 'anh'
            })
        }

    def __init__(self, *args, **kwargs):
        super(BaiVietForm, self).__init__(*args, **kwargs)
        # Đặt các trường bắt buộc
        self.fields['tieu_de'].required = True
        self.fields['duong_dan'].required = True
        self.fields['noi_dung'].required = True
        self.fields['ma_dm'].required = True
        self.fields['ma_the'].required = True
        self.fields['menu'].required = True

        # Các trường không bắt buộc
        self.fields['tom_tat'].required = False
        self.fields['anh'].required = False

    def clean_duong_dan(self):
        """Kiểm tra và chuẩn hóa đường dẫn"""
        duong_dan = self.cleaned_data.get('duong_dan')
        if duong_dan:
            # Loại bỏ khoảng trắng và chuyển thành chữ thường
            duong_dan = duong_dan.strip().lower()
            # Thay thế khoảng trắng bằng dấu gạch ngang
            duong_dan = duong_dan.replace(' ', '-')
        return duong_dan

    def clean(self):
        """Kiểm tra dữ liệu form tổng thể"""
        cleaned_data = super().clean()
        tieu_de = cleaned_data.get('tieu_de')
        duong_dan = cleaned_data.get('duong_dan')

        # Nếu không có đường dẫn nhưng có tiêu đề, tạo đường dẫn từ tiêu đề
        if not duong_dan and tieu_de:
            cleaned_data['duong_dan'] = slugify(tieu_de)

        return cleaned_data

    def save(self, commit=True):
        """
        Ghi đè phương thức save để cập nhật số lượng bài viết trong danh mục và thẻ
        """
        instance = super(BaiVietForm, self).save(commit=False)

        # Lưu instance trước để có thể truy cập các trường sau khi lưu
        if commit:
            # Lấy danh mục và thẻ cũ (nếu đang cập nhật bài viết)
            old_dm = None
            old_the = None

            if instance.pk:  # Nếu đang cập nhật bài viết đã tồn tại
                try:
                    old_instance = BaiViet.objects.get(pk=instance.pk)
                    old_dm = old_instance.ma_dm
                    old_the = old_instance.ma_the
                except BaiViet.DoesNotExist:
                    pass

            # Lưu instance
            instance.save()

            # Cập nhật số lượng bài viết trong danh mục và thẻ
            self._update_count(instance, old_dm, old_the)

        return instance

    def _update_count(self, instance, old_dm=None, old_the=None):
        """
        Cập nhật số lượng bài viết trong danh mục và thẻ
        """
        # Cập nhật danh mục
        if old_dm and old_dm != instance.ma_dm:
            # Giảm số lượng bài viết trong danh mục cũ
            old_dm.so_bai_viet = max(0, old_dm.so_bai_viet - 1)
            old_dm.save()

        # Tăng số lượng bài viết trong danh mục mới
        if not old_dm or old_dm != instance.ma_dm:
            instance.ma_dm.so_bai_viet += 1
            instance.ma_dm.save()

        # Cập nhật thẻ
        if old_the and old_the != instance.ma_the:
            # Giảm số lượng bài viết trong thẻ cũ
            old_the.so_bai_viet = max(0, old_the.so_bai_viet - 1)
            old_the.save()

        # Tăng số lượng bài viết trong thẻ mới
        if not old_the or old_the != instance.ma_the:
            instance.ma_the.so_bai_viet += 1
            instance.ma_the.save()
