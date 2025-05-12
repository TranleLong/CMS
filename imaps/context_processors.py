from csdl.models import DanhMuc


def global_context(request):
    """
    Context processor để cung cấp dữ liệu chung cho tất cả các template
    """
    try:
        # Lấy danh mục cho menu toàn cục
        global_services = DanhMuc.objects.filter(trang_thai=True, parent_id__isnull=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy danh mục toàn cục: {str(e)}")
        global_services = []

    return {
        'global_services': global_services,
    }
