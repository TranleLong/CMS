# imaps_agency/context_processors.py
from csdl.models import DanhMuc


def global_context(request):
    """
    Thêm dữ liệu chung vào context của tất cả các template
    """
    # Lấy danh mục dịch vụ
    services = DanhMuc.objects.filter(
        trang_thai=True,
        parent_id__isnull=True
    ).order_by('order_index')

    return {
        'global_services': services
    }