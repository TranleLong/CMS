from django import forms
from csdl.models import Media
from django.core.validators import FileExtensionValidator


class MediaForm(forms.ModelForm):
    folder_name = forms.CharField(
        max_length=255,
        required=True,
        label='Thư mục',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập tên thư mục'})
    )

    class Meta:
        model = Media
        fields = ['folder_name', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-input',
                                            'accept': 'image/*,video/*,application/pdf,application/msword,application/vnd.ms-excel'})
        }
        labels = {
            'image': 'Tệp tin',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Kiểm tra kích thước file (tối đa 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Kích thước file không được vượt quá 10MB.')

            # Kiểm tra phần mở rộng file
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'svg', 'mp4', 'pdf', 'doc', 'docx', 'xls', 'xlsx']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f'Định dạng file không được hỗ trợ. Các định dạng được hỗ trợ: {", ".join(allowed_extensions)}')
        return image


class FolderForm(forms.Form):
    folder_name = forms.CharField(
        max_length=255,
        required=True,
        label='Tên thư mục',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nhập tên thư mục'})
    )

    description = forms.CharField(
        required=False,
        label='Mô tả',
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Mô tả về thư mục (tùy chọn)'})
    )
