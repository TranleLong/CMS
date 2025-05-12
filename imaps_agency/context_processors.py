# imaps_agency/context_processors.py
from csdl.models import DanhMuc


def global_context(request):
    """
    Thêm dữ liệu chung vào context của tất cả các template
    """
    try:
        # Lấy danh mục dịch vụ
        services = DanhMuc.objects.filter(
            trang_thai=True,
            parent_id__isnull=True
        ).order_by('order_index')


        # Tạo danh sách dịch vụ cứng để đảm bảo luôn có dữ liệu
        hardcoded_services = [
            {'ten_dm': 'Thiết kế website', 'slug': 'thiet-ke-website'},
            {'ten_dm': 'Quảng cáo Google Ads', 'slug': 'quang-cao-google-ads'},
            {'ten_dm': 'Email Marketing', 'slug': 'email-marketing'},
            {'ten_dm': 'SEO', 'slug': 'seo'}
        ]

        return {
            'global_services': services,
            'hardcoded_services': hardcoded_services,
            'services_count': services.count()
        }
    except Exception as e:
        logger.error(f"Error in global_context: {str(e)}")
        # Trả về danh sách cứng nếu có lỗi
        hardcoded_services = [
            {'ten_dm': 'Thiết kế website', 'slug': 'thiet-ke-website'},
            {'ten_dm': 'Quảng cáo Google Ads', 'slug': 'quang-cao-google-ads'},
            {'ten_dm': 'Email Marketing', 'slug': 'email-marketing'},
            {'ten_dm': 'SEO', 'slug': 'seo'}
        ]
        return {
            'global_services': [],
            'hardcoded_services': hardcoded_services,
            'services_count': 0
        }