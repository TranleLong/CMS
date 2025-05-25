from django import forms
from csdl.models import The

class TheForm(forms.ModelForm):
    class Meta:
        model = The
        fields = ['ten_the', 'slug', 'mo_ta']
        widgets = {
            'ten_the': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập tên thẻ'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ten-the'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6, 'placeholder': 'Nhập mô tả cho thẻ'}),
        }
        labels = {
            'ten_the': 'Tên thẻ',
            'slug': 'Đường dẫn',
            'mo_ta': 'Mô tả',
        }
