from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ThanhVienForm(UserCreationForm):
    VAI_TRO_CHOICES = [
        ('nhan_vien', 'Nhân viên'),
        ('quan_ly', 'Quản lý'),
    ]

    vai_tro = forms.ChoiceField(
        choices=VAI_TRO_CHOICES,
        label='Vai trò',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label='Hoạt động',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Tên',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập tên'})
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Họ',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập họ'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'vai_tro', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập tên đăng nhập'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Nhập email'}),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        self.edit_mode = kwargs.pop('edit_mode', False)
        super(ThanhVienForm, self).__init__(*args, **kwargs)

        # Nếu đang ở chế độ chỉnh sửa, không yêu cầu mật khẩu
        if self.edit_mode:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].widget = forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Để trống nếu không thay đổi'
            })
            self.fields['password2'].widget = forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Để trống nếu không thay đổi'
            })
        else:
            self.fields['password1'].widget = forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập mật khẩu'
            })
            self.fields['password2'].widget = forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập lại mật khẩu'
            })

    def clean_password2(self):
        # Nếu đang ở chế độ chỉnh sửa và không nhập mật khẩu, bỏ qua kiểm tra
        if self.edit_mode and not self.cleaned_data.get('password1'):
            return None
        return super(ThanhVienForm, self).clean_password2()
