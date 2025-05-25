from django import forms
from csdl.models import DanhMuc  # Import từ csdl.models thay vì .models

class DanhMucForm(forms.ModelForm):
    class Meta:
        model = DanhMuc
        fields = ['ten_dm', 'slug', 'parent_id', 'mo_ta', 'trang_thai']
        widgets = {
            'ten_dm': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập tên danh mục'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'duong-dan-danh-muc'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, 'placeholder': 'Nhập mô tả cho danh mục'}),
        }
        labels = {
            'ten_dm': 'Tên danh mục',
            'slug': 'Đường dẫn',
            'parent_id': 'Danh mục cha',
            'mo_ta': 'Mô tả',
            'trang_thai': 'Trạng thái',
        }