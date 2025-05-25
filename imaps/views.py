from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from grpc.framework.common.style import Service

from csdl.models import BaiViet, DanhMuc, Menu, The, MenuBaiViet
from csdl.models import Contact
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from quanlymenu.views import get_header_menus


def home(request):
    header_menus = get_header_menus()
    # Lấy danh sách danh mục (dịch vụ) cho trang chủ
    try:
        services = DanhMuc.objects.filter(
            trang_thai=True,
            parent_id__isnull=True
        ).order_by('order_index')
    except Exception as e:
        services = []

    # Lấy bài viết nổi bật
    try:
        featured_articles = BaiViet.objects.filter(
            trang_thai='Đã duyệt',
            ngay_dang__lte=timezone.now().date()
        ).select_related('ma_dm', 'ma_the', 'ma_nguoi_dung').order_by('-ngay_dang')
    except Exception as e:
        featured_articles = []

    # Lấy bài viết mới nhất - Chỉ lấy những bài viết có trạng thái "đã duyệt"
    try:
        # Lấy bài viết có trạng thái "đã duyệt" (published)
        latest_articles = BaiViet.objects.filter(
            trang_thai='Đã duyệt'  # Chỉ lấy bài viết đã duyệt
        ).select_related('ma_dm', 'ma_the', 'ma_nguoi_dung').order_by(
            '-ngay_dang')[:3]  # Sắp xếp theo ngày đăng giảm dần (mới nhất lên đầu)
    except Exception as e:
        latest_articles = []
    context = {
        'header_menus': header_menus,  # Thêm menu cho header
        'services': services,
        'featured_articles': featured_articles, # list chứa các bài viết
        'latest_articles': latest_articles,
        # 'all_categories': all_categories,  # Thêm danh mục cho menu dropdown
    }
    return render(request, 'home.html', context)

def contact(request):
    # Lấy danh sách menu cho header
    header_menus = get_header_menus()
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ho_ten = request.POST.get('ho_ten')
        email = request.POST.get('email')
        so_dien_thoai = request.POST.get('so_dien_thoai')
        chu_de = request.POST.get('chu_de')
        noi_dung = request.POST.get('noi_dung')

        # Tạo đối tượng Contact mới
        contact = Contact(
            ho_ten=ho_ten,
            email=email,
            so_dien_thoai=so_dien_thoai,
            chu_de=chu_de,
            noi_dung=noi_dung,
            ngay_gui=timezone.now()
        )
        # Lưu vào cơ sở dữ liệu
        contact.save()
        # Hiển thị thông báo thành công
        messages.success(request,'Cảm ơn bạn đã liên hệ với chúng tôi. Chúng tôi sẽ phản hồi trong thời gian sớm nhất!')
        # Chuyển hướng về trang liên hệ
        return redirect('contact')

    # Nếu là GET request, hiển thị trang liên hệ
    context = {
        'header_menus': header_menus,  # Thêm menu cho header
    }
    return render(request, 'contact.html', context)


def service_detail(request, slug):
    """
    Hiển thị chi tiết dịch vụ và nội dung bài viết đầu tiên thuộc danh mục đó
    """
    # Lấy danh sách menu cho header
    header_menus = get_header_menus()

    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    # Lấy thông tin dịch vụ theo slug
    print(f"DEBUG: Đang tìm danh mục với slug: {slug}")
    try:
        service = get_object_or_404(DanhMuc, slug=slug, trang_thai=True)
        print(f"DEBUG: Tìm thấy danh mục: {service.ten_dm}, ID: {service.ma_dm}, Slug: {service.slug}")

        # Lấy các bài viết thuộc danh mục này
        articles = BaiViet.objects.filter(
            ma_dm=service,
            trang_thai='Đã duyệt',
        ).select_related('ma_dm', 'ma_the', 'ma_nguoi_dung').order_by('-ngay_dang')

        print(f"DEBUG: Số lượng bài viết tìm thấy trong danh mục {service.ten_dm}: {articles.count()}")

        # Lấy bài viết đầu tiên để hiển thị nội dung
        first_article = None
        if articles.exists():
            first_article = articles.first()
            print(f"DEBUG: Bài viết đầu tiên: {first_article.tieu_de}")
        else:
            print(f"DEBUG: Không tìm thấy bài viết nào có trạng thái 'Đã duyệt' cho danh mục {service.ten_dm}")

        # Lấy các thẻ liên quan đến các bài viết trong danh mục
        tags = The.objects.filter(baiviet__ma_dm=service).distinct()

        # Lọc theo thẻ nếu có
        tag_filter = request.GET.get('tag')
        if tag_filter:
            try:
                tag = get_object_or_404(The, slug=tag_filter)
                articles = articles.filter(ma_the=tag)
                # Cập nhật bài viết đầu tiên nếu có lọc theo thẻ
                if articles.exists():
                    first_article = articles.first()
                current_tag = tag
            except Exception as e:
                print(f"Lỗi khi lọc bài viết theo thẻ: {str(e)}")
                current_tag = None
        else:
            current_tag = None

    except Exception as e:
        print(f"Lỗi khi lấy chi tiết dịch vụ: {str(e)}")
        messages.error(request, "Không tìm thấy dịch vụ hoặc có lỗi xảy ra.")
        return redirect('home')

    context = {
        'header_menus': header_menus,  # Thêm menu cho header
        'all_categories': all_categories,
        'service': service,
        'articles': articles,
        'first_article': first_article,  # Thêm bài viết đầu tiên vào context
        'tags': tags,
        'current_tag': current_tag,
    }
    return render(request, 'service_detail.html', context)


def article_detail(request, slug):
    # Lấy danh sách menu cho header
    header_menus = get_header_menus()

    # Lấy tất cả danh mục cho menu dropdown
    try:
        all_categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')
    except Exception as e:
        print(f"Lỗi khi lấy tất cả danh mục: {str(e)}")
        all_categories = []

    # Chuẩn hóa slug
    if slug.startswith('/'):
        slug = slug[1:]
    if slug.endswith('/'):
        slug = slug[:-1]

    # Loại bỏ tiền tố "bai-viet/" nếu có
    if slug.startswith('bai-viet/'):
        slug = slug[9:]

    print(f"DEBUG: Tìm kiếm bài viết với slug đã chuẩn hóa: '{slug}'")

    # Tìm bài viết theo đường dẫn - thử nhiều cách khác nhau
    article = None
    try:
        # Cách 1: Tìm chính xác
        article = BaiViet.objects.get(Q(duong_dan=slug) | Q(duong_dan='/' + slug), trang_thai='Đã duyệt')
    except BaiViet.DoesNotExist:
        try:
            # Cách 2: Tìm với các biến thể khác
            article = BaiViet.objects.filter(
                Q(duong_dan=slug) |
                Q(duong_dan='/' + slug) |
                Q(duong_dan__endswith='/' + slug) |
                Q(duong_dan__contains=slug),
                trang_thai='Đã duyệt'
            ).first()
        except Exception as e:
            print(f"DEBUG: Lỗi khi tìm bài viết cách 2: {str(e)}")
    except Exception as e:
        print(f"DEBUG: Lỗi khi tìm bài viết: {str(e)}")

    if article:
        print(f"DEBUG: Tìm thấy bài viết: {article.tieu_de}, Trạng thái: {article.trang_thai}")

        # Kiểm tra xem article.ma_dm có tồn tại và có slug không
        if article.ma_dm:
            print(f"DEBUG: Bài viết thuộc danh mục: {article.ma_dm.ten_dm}")
        else:
            print(f"DEBUG: Bài viết không có danh mục")

        # Lấy các bài viết liên quan
        related_articles = []
        if article.ma_dm:
            related_articles = BaiViet.objects.filter(
                ma_dm=article.ma_dm,
                trang_thai="Đã duyệt",
            ).exclude(ma_bv=article.ma_bv).order_by('-ngay_dang')[:3]

        # Lấy các thẻ phổ biến
        popular_tags = The.objects.all().order_by('-so_bai_viet')[:10]
    else:
        print(f"DEBUG: Không tìm thấy bài viết với đường dẫn: {slug}")
        messages.error(request, "Không tìm thấy bài viết hoặc bài viết chưa được duyệt.")
        return redirect('home')

    context = {
        'header_menus': header_menus,
        'all_categories': all_categories,
        'article': article,
        'related_articles': related_articles,
        'popular_tags': popular_tags,
        'categories': all_categories,
    }
    return render(request, 'article_detail.html', context)



