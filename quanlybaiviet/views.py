from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from csdl.models import BaiViet, DanhMuc, The, Media, BaiVietMedia
import os


# Quản lý bài viết
@login_required(login_url='login')
def quanlybaiviet(request):
    # Lấy tham số từ URL
    search_query = request.GET.get('search', '')
    danh_muc = request.GET.get('danh_muc', '')
    trang_thai = request.GET.get('trang_thai', '')
    menu = request.GET.get('menu', '')  # Thêm tham số lọc theo menu
    danh_muc_list = DanhMuc.objects.all()
    # Lọc bài viết theo người dùng hiện tại và các bộ lọc khác
    # Kiểm tra nhóm người dùng
    is_manager = request.user.groups.filter(id=1).exists()

    # Lọc bài viết theo từ khóa tìm kiếm và các bộ lọc
    if is_manager:
        # Nếu là quản lý (group_id = 1), hiển thị tất cả bài viết
        bai_viet_list = BaiViet.objects.all().order_by('-ngay_dang')
    else:
        # Nếu là nhân viên (group_id = 2), chỉ hiển thị bài viết của người dùng đó
        bai_viet_list = BaiViet.objects.filter(ma_nguoi_dung=request.user).order_by('-ngay_dang')

    if danh_muc:
        bai_viet_list = bai_viet_list.filter(ma_dm=danh_muc)

    if trang_thai:
        bai_viet_list = bai_viet_list.filter(trang_thai=trang_thai)

    if menu:
        bai_viet_list = bai_viet_list.filter(menu=menu)

    # Phân trang
    paginator = Paginator(bai_viet_list, 10)  # 10 bài viết mỗi trang
    page_number = request.GET.get('page', 1)
    bai_viet_page = paginator.get_page(page_number)
    published_count = BaiViet.objects.filter(trang_thai='Đã duyệt').count()
    pending_count = BaiViet.objects.filter(trang_thai='Chờ duyệt').count()
    draft_count = BaiViet.objects.filter(trang_thai='Bản nháp').count()
    context = {
        'bai_viet_list': bai_viet_page,
        'search_query': search_query,
        'selected_danh_muc': danh_muc,
        'selected_trang_thai': trang_thai,
        # 'selected_menu': menu,  # Thêm selected_menu vào context
        'total_count': bai_viet_list.count(),
        'danh_muc_list': danh_muc_list,
        'bai_viet_list': bai_viet_list,
        'published_count': published_count,
        'pending_count': pending_count,
        'draft_count': draft_count,

    }

    return render(request, 'quanlybaiviet.html', context)

@login_required(login_url='login')
def xem_baiviet(request, bai_viet_id):
    # Lấy thông tin bài viết
    bai_viet = get_object_or_404(BaiViet, ma_bv=bai_viet_id)

    # Lấy danh sách bài viết liên quan (cùng danh mục)
    bai_viet_lien_quan = BaiViet.objects.filter(ma_dm=bai_viet.ma_dm).exclude(ma_bv=bai_viet_id)[:5]

    context = {
        'bai_viet': bai_viet,
        'bai_viet_lien_quan': bai_viet_lien_quan,
    }

    return render(request, 'xembaiviet.html', context)
# API để lấy danh sách media
def api_media_list(request):
    """
    API để lấy danh sách media cho modal chọn ảnh
    """
    media_type = request.GET.get('type', None)
    search_query = request.GET.get('search', '')

    # Lọc media theo loại và tìm kiếm
    media_query = Media.objects.all().order_by('-ma_media')

    if media_type:
        media_query = media_query.filter(type_name=media_type)

    if search_query:
        media_query = media_query.filter(file_name__icontains=search_query)

    # Giới hạn số lượng kết quả
    media_list = media_query[:50]

    # Chuẩn bị dữ liệu trả về với URL tuyệt đối
    media_data = []
    for media in media_list:
        # Đảm bảo URL là tuyệt đối bằng cách sử dụng build_absolute_uri
        media_url = request.build_absolute_uri(media.image.url) if media.image else ''
        media_data.append({
            'id': media.ma_media,
            'name': media.file_name,
            'type': media.type_name,
            'size': media.size,
            'folder': media.folder_name,
            'url': media_url,
        })

    return JsonResponse({
        'success': True,
        'media': media_data
    })


# Lấy URL của một media cụ thể
def get_media_url(request, media_id):
    """
    Lấy URL đầy đủ cho một media item
    """
    try:
        media = Media.objects.get(ma_media=media_id)
        if media.image:
            return JsonResponse({
                'success': True,
                'url': request.build_absolute_uri(media.image.url),
                'name': media.file_name
            })
        return JsonResponse({
            'success': False,
            'message': 'Media không có ảnh'
        })
    except Media.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Không tìm thấy media'
        }, status=404)


@login_required
def xoa_baiviet(request, bai_viet_id):
    bai_viet = get_object_or_404(BaiViet, ma_bv=bai_viet_id)

    # Kiểm tra quyền xóa bài viết
    is_admin = request.user.is_superuser or request.user.groups.filter(id=1).exists()
    is_author = bai_viet.ma_nguoi_dung == request.user

    if not is_admin and not is_author:
        return JsonResponse({
            'success': False,
            'message': 'Bạn không có quyền xóa bài viết này!'
        }, status=403)

    if request.method == 'POST':
        try:
            bai_viet.delete()
            return JsonResponse({'success': True, 'message': 'Xóa bài viết thành công!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Lỗi khi xóa bài viết: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Phương thức không được hỗ trợ'})


@login_required(login_url='login')
def them_baiviet(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        tieu_de = request.POST.get('tieu_de')
        duong_dan = request.POST.get('duong_dan')
        tom_tat = request.POST.get('tom_tat', '')
        noi_dung = request.POST.get('noi_dung')
        ma_dm = request.POST.get('ma_dm')
        ma_the = request.POST.get('ma_the')
        trang_thai = request.POST.get('trang_thai', 'Bản nháp')

        # Xử lý ảnh đại diện
        anh = request.FILES.get('anh')
        selected_media_id = request.POST.get('selected_media_id')

        # Tạo bài viết mới
        bai_viet = BaiViet(
            tieu_de=tieu_de,
            duong_dan=duong_dan,
            tom_tat=tom_tat,
            noi_dung=noi_dung,
            ma_dm_id=ma_dm,
            ma_the_id=ma_the,
            trang_thai=trang_thai,
            ngay_dang=timezone.now().date(),
            ma_nguoi_dung=request.user
        )

        # Xử lý ảnh đại diện
        if anh:
            bai_viet.anh = anh

            # Lưu bài viết trước để có ID
            bai_viet.save()

            # Tạo bản ghi Media mới
            file_name = os.path.basename(anh.name)
            file_size = anh.size
            file_type = 'image'

            # Tạo Media mới
            media = Media(
                folder_name='bai_viet',
                file_name=file_name,
                type_name=file_type,
                size=file_size,
                image=anh,  # Sử dụng cùng file ảnh
                ma_nguoi_dung=request.user
            )
            media.save()

            # Tạo liên kết BaiVietMedia
            bai_viet_media = BaiVietMedia(
                ma_bv=bai_viet,
                ma_media=media
            )
            bai_viet_media.save()

        elif selected_media_id:
            try:
                media = Media.objects.get(ma_media=selected_media_id)
                bai_viet.anh = media.image
                bai_viet.save()

                # Tạo liên kết với media
                bai_viet_media = BaiVietMedia(
                    ma_bv=bai_viet,
                    ma_media=media
                )
                bai_viet_media.save()
            except Media.DoesNotExist:
                bai_viet.save()
        else:
            bai_viet.save()

        messages.success(request, "Thêm bài viết thành công!")
        return redirect('quanlybaiviet')

    # Lấy danh sách danh mục và thẻ để hiển thị trong form
    danh_muc_list = DanhMuc.objects.all()
    the_list = The.objects.all()

    context = {
        'danh_muc_list': danh_muc_list,
        'the_list': the_list,
    }

    return render(request, 'thembaiviet.html', context)


@login_required(login_url='login')
def sua_baiviet(request, bai_viet_id):
    # Lấy thông tin bài viết
    bai_viet = get_object_or_404(BaiViet, ma_bv=bai_viet_id)

    # Kiểm tra quyền sửa bài viết
    is_admin = request.user.is_superuser or request.user.groups.filter(id=1).exists()
    is_author = bai_viet.ma_nguoi_dung == request.user

    if not is_admin and not is_author:
        messages.error(request, "Bạn không có quyền sửa bài viết này!")
        return redirect('quanlybaiviet')
    elif request.method == 'POST':
        # Lấy dữ liệu từ form
        tieu_de = request.POST.get('tieu_de')
        duong_dan = request.POST.get('duong_dan')
        tom_tat = request.POST.get('tom_tat', '')
        noi_dung = request.POST.get('noi_dung')
        ma_dm = request.POST.get('ma_dm')
        ma_the = request.POST.get('ma_the')
        trang_thai = request.POST.get('trang_thai', 'Bản nháp')

        # Xử lý ảnh đại diện
        anh = request.FILES.get('anh')
        selected_media_id = request.POST.get('selected_media_id')

        # Cập nhật bài viết
        bai_viet.tieu_de = tieu_de
        bai_viet.duong_dan = duong_dan
        bai_viet.tom_tat = tom_tat
        bai_viet.noi_dung = noi_dung
        bai_viet.ma_dm_id = ma_dm
        bai_viet.ma_the_id = ma_the
        bai_viet.trang_thai = trang_thai

        # Xử lý ảnh đại diện
        if anh:
            # Xóa ảnh cũ nếu có
            if bai_viet.anh:
                if os.path.isfile(bai_viet.anh.path):
                    os.remove(bai_viet.anh.path)

            bai_viet.anh = anh
            bai_viet.save()

            # Tạo bản ghi Media mới
            file_name = os.path.basename(anh.name)
            file_size = anh.size
            file_type = 'image'

            # Tạo Media mới
            media = Media(
                folder_name='bai_viet',
                file_name=file_name,
                type_name=file_type,
                size=file_size,
                image=anh,  # Sử dụng cùng file ảnh
                ma_nguoi_dung=request.user
            )
            media.save()

            # Tạo liên kết BaiVietMedia
            bai_viet_media = BaiVietMedia(
                ma_bv=bai_viet,
                ma_media=media
            )
            bai_viet_media.save()

        elif selected_media_id:
            try:
                media = Media.objects.get(ma_media=selected_media_id)
                # Xóa ảnh cũ nếu có
                if bai_viet.anh:
                    if os.path.isfile(bai_viet.anh.path):
                        os.remove(bai_viet.anh.path)
                bai_viet.anh = media.image
                bai_viet.save()

                # Tạo liên kết với media
                if not BaiVietMedia.objects.filter(ma_bv=bai_viet, ma_media=media).exists():
                    bai_viet_media = BaiVietMedia(
                        ma_bv=bai_viet,
                        ma_media=media
                    )
                    bai_viet_media.save()
            except Media.DoesNotExist:
                bai_viet.save()
        else:
            bai_viet.save()

        messages.success(request, "Cập nhật bài viết thành công!")
        return redirect('quanlybaiviet')

    # Lấy danh sách danh mục và thẻ để hiển thị trong form
    danh_muc_list = DanhMuc.objects.all()
    the_list = The.objects.all()

    context = {
        'bai_viet': bai_viet,
        'danh_muc_list': danh_muc_list,
        'the_list': the_list,
    }

    return render(request, 'suabaiviet.html', context)