from django import forms
from csdl.models import Menu, BaiViet
from django.utils.text import slugify


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['tieu_de', 'slug', 'trang_thai']
        labels = {
            'tieu_de': 'Tiêu đề',
            'slug': 'Đường dẫn',
            'trang_thai': 'Trạng thái'
        }
        widgets = {
            'tieu_de': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tiêu đề menu',
                'id': 'menuTitle'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'duong-dan-menu',
                'id': 'menuSlug'
            }),
            'trang_thai': forms.Select(attrs={
                'class': 'form-select',
                'id': 'trang_thai'
            }, choices=[
                ('Dang hoat dong', 'Đang hoạt động'),
                ('Khong hoat dong', 'Không hoạt động')
            ])
        }

    # Field để lưu trữ các bài viết được chọn
    bai_viet_ids = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'bai-viet-checkbox'
        }),
        label='Bài viết liên quan'
    )

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        # Lấy danh sách bài viết để hiển thị trong form
        bai_viet_choices = [(str(bv.ma_bv), bv.tieu_de) for bv in BaiViet.objects.all().order_by('-ngay_dang')]
        self.fields['bai_viet_ids'].choices = bai_viet_choices

        # Nếu đang sửa menu, đánh dấu các bài viết đã được chọn
        if self.instance.pk:
            selected_bai_viet = BaiViet.objects.filter(menu=self.instance).values_list('ma_bv', flat=True)
            self.initial['bai_viet_ids'] = [str(bv_id) for bv_id in selected_bai_viet]

    def clean_slug(self):
        """Kiểm tra và chuẩn hóa slug"""
        slug = self.cleaned_data.get('slug')
        if slug:
            # Loại bỏ khoảng trắng và chuyển thành chữ thường
            slug = slug.strip().lower()
            # Thay thế khoảng trắng bằng dấu gạch ngang
            slug = slug.replace(' ', '-')
        return slug

    def clean(self):
        """Kiểm tra dữ liệu form tổng thể"""
        cleaned_data = super().clean()
        tieu_de = cleaned_data.get('tieu_de')
        slug = cleaned_data.get('slug')

        # Nếu không có slug nhưng có tiêu đề, tạo slug từ tiêu đề
        if not slug and tieu_de:
            cleaned_data['slug'] = slugify(tieu_de)

        return cleaned_data
