from django.shortcuts import render
from django.utils import timezone
from csdl.models import BaiViet, DanhMuc, Menu, The


def home(request):
    """
    Hiển thị trang chủ với danh sách dịch vụ và bài viết nổi bật
    """
    # Lấy danh sách danh mục (dịch vụ) cho trang chủ
    try:
        services = DanhMuc.objects.filter(
            trang_thai=True,
            parent_id__isnull=True
        ).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy danh mục dịch vụ: {str(e)}")
        services = []

    # Lấy bài viết nổi bật
    try:
        featured_articles = BaiViet.objects.filter(
            trang_thai='published',
            ngay_dang__lte=timezone.now().date()
        ).select_related('ma_dm', 'ma_the', 'ma_nguoi_dung', 'menu').order_by('-ngay_dang')[:3]
    except Exception as e:
        print(f"Lỗi khi lấy bài viết nổi bật: {str(e)}")
        featured_articles = []

    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    context = {
        'services': services,
        'featured_articles': featured_articles,
        'all_categories': all_categories,  # Thêm danh mục cho menu dropdown
    }
    return render(request, 'home.html', context)


def about(request):
    """
    Hiển thị trang giới thiệu
    """
    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'about.html', context)


def mission(request):
    """
    Hiển thị trang sứ mệnh
    """
    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'mission.html', context)


def contact(request):
    """
    Hiển thị trang liên hệ
    """
    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    # Xử lý form liên hệ nếu có
    if request.method == 'POST':
        # Xử lý form ở đây
        pass

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'contact.html', context)


def service_detail(request, slug):
    """
    Hiển thị chi tiết dịch vụ
    """
    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    # Lấy thông tin dịch vụ theo slug
    try:
        service = DanhMuc.objects.get(slug=slug, trang_thai=True)

        # Lấy các bài viết thuộc danh mục này
        articles = BaiViet.objects.filter(
            ma_dm=service,
            trang_thai='published',
            ngay_dang__lte=timezone.now().date()
        ).select_related('ma_dm', 'ma_the', 'ma_nguoi_dung', 'menu').order_by('-ngay_dang')
    except Exception as e:
        print(f"Lỗi khi lấy chi tiết dịch vụ: {str(e)}")
        service = None
        articles = []

    context = {
        'all_categories': all_categories,
        'service': service,
        'articles': articles,
    }
    return render(request, 'service_detail.html', context)


def article_detail(request, slug):
    """
    Hiển thị chi tiết bài viết
    """
    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    # Lấy thông tin bài viết theo slug
    try:
        article = BaiViet.objects.get(duong_dan=slug, trang_thai='published')

        # Lấy các bài viết liên quan
        related_articles = BaiViet.objects.filter(
            ma_dm=article.ma_dm,
            trang_thai='published',
            ngay_dang__lte=timezone.now().date()
        ).exclude(ma_bv=article.ma_bv).select_related('ma_dm', 'ma_the', 'ma_nguoi_dung', 'menu').order_by(
            '-ngay_dang')[:3]

        # Lấy các thẻ phổ biến
        popular_tags = The.objects.all().order_by('-so_bai_viet')[:10]

    except Exception as e:
        print(f"Lỗi khi lấy chi tiết bài viết: {str(e)}")
        article = None
        related_articles = []
        popular_tags = []

    context = {
        'all_categories': all_categories,
        'article': article,
        'related_articles': related_articles,
        'popular_tags': popular_tags,
        'categories': all_categories,  # Sử dụng all_categories cho sidebar
    }
    return render(request, 'article_detail.html', context)
