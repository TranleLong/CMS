from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from csdl.models import BaiViet, DuyetBaiViet
from csdl.models import DanhMuc
from csdl.models import The
from csdl.models import Media
from .forms import ContactForm


def home(request):
    # Lấy các bài viết đã được duyệt và đã đăng
    featured_articles = BaiViet.objects.filter(
        trang_thai='published',
        ngay_dang__lte=timezone.now().date()
    ).order_by('-ngay_dang')[:3]

    # Lấy các bài viết mới nhất
    recent_articles = BaiViet.objects.filter(
        trang_thai='published',
        ngay_dang__lte=timezone.now().date()
    ).order_by('-ngay_dang')[:6]

    context = {
        'featured_articles': featured_articles,
        'recent_articles': recent_articles,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


def mission(request):
    return render(request, 'pages/mission.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Xử lý dữ liệu form ở đây (có thể lưu vào database hoặc gửi email)
            messages.success(request, 'Tin nhắn của bạn đã được gửi thành công!')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'pages/contact.html', context)


def service_detail(request, slug):
    # Lấy danh mục dịch vụ theo slug
    service = get_object_or_404(DanhMuc, slug=slug, trang_thai=True)

    # Lấy các bài viết thuộc danh mục này
    articles = BaiViet.objects.filter(
        ma_dm=service,
        trang_thai='published',
        ngay_dang__lte=timezone.now().date()
    ).order_by('-ngay_dang')

    # Lấy các thẻ liên quan đến các bài viết trong danh mục
    tags = The.objects.filter(baiviet__ma_dm=service).distinct()

    # Lọc theo thẻ nếu có
    tag_filter = request.GET.get('tag')
    if tag_filter:
        tag = get_object_or_404(The, slug=tag_filter)
        articles = articles.filter(ma_the=tag)

    context = {
        'service': service,
        'articles': articles,
        'tags': tags,
        'current_tag': tag_filter,
    }

    # Render template tương ứng với slug của dịch vụ
    template_name = f'services/{slug.replace("-", "_")}.html'

    # Kiểm tra xem template có tồn tại không, nếu không thì sử dụng template mặc định
    try:
        return render(request, template_name, context)
    except:
        return render(request, 'services/default.html', context)


def article_detail(request, slug):
    # Lấy bài viết theo đường dẫn
    article = get_object_or_404(BaiViet, duong_dan=slug, trang_thai='published')

    # Lấy các bài viết liên quan (cùng danh mục)
    related_articles = BaiViet.objects.filter(
        ma_dm=article.ma_dm,
        trang_thai='published',
        ngay_dang__lte=timezone.now().date()
    ).exclude(ma_bv=article.ma_bv).order_by('-ngay_dang')[:3]

    # Lấy tất cả danh mục
    categories = DanhMuc.objects.filter(trang_thai=True).order_by('order_index')

    # Lấy các thẻ phổ biến
    popular_tags = The.objects.all().order_by('-so_bai_viet')[:10]

    context = {
        'article': article,
        'related_articles': related_articles,
        'categories': categories,
        'popular_tags': popular_tags,
    }
    return render(request, 'articles/detail.html', context)