from django.contrib import admin
from csdl.models import Contact

# Đăng ký model Contact vào trang admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'email', 'so_dien_thoai', 'chu_de', 'ngay_gui')
    list_filter = ('chu_de', 'ngay_gui')
    search_fields = ('ho_ten', 'email', 'so_dien_thoai', 'noi_dung')
    date_hierarchy = 'ngay_gui'
    readonly_fields = ('ngay_gui',)
    fieldsets = (
        ('Thông tin người gửi', {
            'fields': ('ho_ten', 'email', 'so_dien_thoai')
        }),
        ('Nội dung liên hệ', {
            'fields': ('chu_de', 'noi_dung', 'ngay_gui')
        }),
        ('Xử lý', {
            'fields': ('ghi_chu',)
        }),
    )
