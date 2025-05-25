from django import forms
from django.utils import timezone
from csdl.models import Menu, BaiViet, DanhMuc, The


class MenuForm(forms.ModelForm):
    url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-input',
            'placeholder': 'https://example.com',
            'id': 'id_url'
        })
    )

    loai_menu = forms.ChoiceField(
        choices=[('bai_viet', 'Bài viết'), ('duong_dan', 'Đường dẫn')],
        widget=forms.RadioSelect(attrs={'class': 'menu-type-radio'}),
        initial='bai_viet'
    )

    class Meta:
        model = Menu
        fields = ['tieu_de', 'slug', 'trang_thai', 'loai_menu', 'url']
        widgets = {
            'tieu_de': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tiêu đề menu',
                'id': 'id_tieu_de'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'duong-dan-menu',
                'id': 'id_slug'
            }),
            'trang_thai': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class MenuItemForm(forms.Form):
    bai_viet_ids = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bai-viet-checkbox'})
    )

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        # Lấy danh sách bài viết để hiển thị trong form
        bai_viet_list = BaiViet.objects.filter(trang_thai='Đã duyệt').order_by('-ngay_dang')
        self.fields['bai_viet_ids'].choices = [(bv.ma_bv, bv.tieu_de) for bv in bai_viet_list]
