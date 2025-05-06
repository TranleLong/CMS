# from django.shortcuts import render
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
#
# from csdl.models import DanhMuc
#
#
# # Create your views here.
# def qlbaiviet(request):
#     return render(request,"quanlybaiviet.html")
# def get_content(request, target):
#     if target == 'quanlybaiviet':
#         # Trả về nội dung block bài viết
#         context = {
#             'baiviet_data': 'Nội dung bài viết mặc định'
#         }
#         return render(request, 'quanlybaiviet.html', context)
#
#     elif target == 'dashboard':
#         context = {
#             'dashboard_data': 'Nội dung dashboard'
#         }
#         return render(request, 'dashboard.html', context)
#     elif target == 'quanlythe':
#         context = {
#             'the_data': 'Nội dung quanlythe'
#         }
#         return render(request, 'quanlythe.html', context)
#     elif target == 'quanlymedia':
#         context = {
#             'media_data': 'Nội dung quanlymedia'
#         }
#         return render(request, 'quanlymedia.html', context)
#     elif target == 'quanlythanhvien':
#         context = {
#             'thanhvien_data': 'Nội dung quanlythanhvien'
#         }
#         return render(request, 'quanlythanhvien.html', context)
#     elif target == 'quanlycauhinh':
#         context = {
#             'cauhinh_data': 'Nội dung quanlycauhinh'
#         }
#         return render(request, 'quanlycauhinh.html', context)
#     elif target == 'quanlymenu':
#         context = {
#             'quanlymenu_data': 'Nội dung menu'
#         }
#         return render(request, 'quanlymenu.html', context)
#     else:
#         # Trường hợp mặc định khi không có target nào khớp
#         return HttpResponse(f"Không tìm thấy trang: {target}", status=404)
#
# def sua_baiviet(request, target):
#     return render(request, 'suabaiviet.html')
# def them_baiviet(request, target):
#     return render(request, 'thembaiviet.html')
# def xem_baiviet(request, target):
#     return render(request, 'xembaiviet.html')
#
#
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from csdl.models import BaiViet, DanhMuc, The
from datetime import datetime
import os


def quanlybaiviet(request):
    # Lấy tham số từ URL
    search_query = request.GET.get('search', '')
    danh_muc = request.GET.get('danh_muc', '')
    trang_thai = request.GET.get('trang_thai', '')

    # Lọc bài viết theo từ khóa tìm kiếm và các bộ lọc
    bai_viet_list = BaiViet.objects.all().order_by('-ngay_dang')

    if search_query:
        bai_viet_list = bai_viet_list.filter(
            Q(tieu_de__icontains=search_query) |
            Q(tom_tat__icontains=search_query)
        )

    if danh_muc:
        bai_viet_list = bai_viet_list.filter(ma_dm=danh_muc)

    if trang_thai:
        bai_viet_list = bai_viet_list.filter(trang_thai=trang_thai)

    # Phân trang
    paginator = Paginator(bai_viet_list, 10)  # 10 bài viết mỗi trang
    page_number = request.GET.get('page', 1)
    bai_viet_page = paginator.get_page(page_number)

    # Lấy danh sách danh mục để hiển thị trong bộ lọc
    danh_muc_list = DanhMuc.objects.all()

    context = {
        'bai_viet_list': bai_viet_page,
        'danh_muc_list': danh_muc_list,
        'search_query': search_query,
        'selected_danh_muc': danh_muc,
        'selected_trang_thai': trang_thai,
        'total_count': bai_viet_list.count(),
    }

    return render(request, 'quanlybaiviet.html', context)


def them_baiviet(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        tieu_de = request.POST.get('tieu_de')
        duong_dan = request.POST.get('duong_dan')
        tom_tat = request.POST.get('tom_tat')
        noi_dung = request.POST.get('noi_dung')
        ma_dm = request.POST.get('ma_dm')
        ma_the = request.POST.get('ma_the')
        trang_thai = request.POST.get('trang_thai', 'Chờ duyệt')  # Mặc định là Chờ duyệt

        # Xử lý ảnh đại diện nếu có
        anh = None
        if 'anh' in request.FILES:
            anh = request.FILES['anh']

        # Kiểm tra dữ liệu
        if not tieu_de or not duong_dan or not noi_dung or not ma_dm or not ma_the:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin bài viết.")
            return redirect('them_baiviet')

        # Lấy user hiện tại hoặc user mặc định
        try:
            user = request.user
            if not user.is_authenticated:
                user = User.objects.first()  # Lấy user đầu tiên nếu không có user đăng nhập
                if not user:
                    # Tạo user mặc định nếu không có user nào
                    user = User.objects.create_user(
                        username='default_user',
                        password='default_password',
                        email='default@example.com'
                    )
        except:
            # Nếu có lỗi, tạo một user mặc định
            user = User.objects.create_user(
                username='default_user',
                password='default_password',
                email='default@example.com'
            )

        # Lấy đối tượng DanhMuc và The
        danh_muc = get_object_or_404(DanhMuc, ma_dm=ma_dm)
        the = get_object_or_404(The, ma_the=ma_the)

        # Tạo bài viết mới
        bai_viet = BaiViet(
            tieu_de=tieu_de,
            duong_dan=duong_dan,
            tom_tat=tom_tat,
            noi_dung=noi_dung,
            trang_thai=trang_thai,
            ngay_dang=datetime.now().date(),
            ma_nguoi_dung=user,
            ma_dm=danh_muc,
            ma_the=the,
            anh=anh
        )

        # Lưu bài viết
        bai_viet.save()

        messages.success(request, "Bài viết đã được thêm thành công!")
        return redirect('quanlybaiviet')

    # Lấy danh sách danh mục và thẻ để hiển thị trong form
    danh_muc_list = DanhMuc.objects.all()
    the_list = The.objects.all()

    context = {
        'danh_muc_list': danh_muc_list,
        'the_list': the_list,
    }

    return render(request, 'thembaiviet.html', context)


def xem_baiviet(request, bai_viet_id):
    # Lấy thông tin bài viết từ cơ sở dữ liệu
    bai_viet = get_object_or_404(BaiViet, ma_bv=bai_viet_id)

    # Lấy các bài viết liên quan (cùng danh mục)
    bai_viet_lien_quan = BaiViet.objects.filter(ma_dm=bai_viet.ma_dm).exclude(ma_bv=bai_viet_id)[:3]

    context = {
        'bai_viet': bai_viet,
        'bai_viet_lien_quan': bai_viet_lien_quan,
    }

    return render(request, 'xembaiviet.html', context)


def sua_baiviet(request, bai_viet_id):
    # Lấy thông tin bài viết từ cơ sở dữ liệu
    bai_viet = get_object_or_404(BaiViet, ma_bv=bai_viet_id)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        tieu_de = request.POST.get('tieu_de')
        duong_dan = request.POST.get('duong_dan')
        tom_tat = request.POST.get('tom_tat')
        noi_dung = request.POST.get('noi_dung')
        ma_dm = request.POST.get('ma_dm')
        ma_the = request.POST.get('ma_the')
        trang_thai = request.POST.get('trang_thai')

        # Kiểm tra dữ liệu
        if not tieu_de or not duong_dan or not noi_dung or not ma_dm or not ma_the:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin bài viết.")
            return redirect('sua_baiviet', bai_viet_id=bai_viet_id)

        # Cập nhật thông tin bài viết
        bai_viet.tieu_de = tieu_de
        bai_viet.duong_dan = duong_dan
        bai_viet.tom_tat = tom_tat
        bai_viet.noi_dung = noi_dung
        bai_viet.trang_thai = trang_thai

        # Cập nhật danh mục và thẻ
        bai_viet.ma_dm = get_object_or_404(DanhMuc, ma_dm=ma_dm)
        bai_viet.ma_the = get_object_or_404(The, ma_the=ma_the)

        # Xử lý ảnh đại diện nếu có
        if 'anh' in request.FILES:
            # Xóa ảnh cũ nếu có
            if bai_viet.anh:
                if os.path.isfile(bai_viet.anh.path):
                    os.remove(bai_viet.anh.path)

            # Cập nhật ảnh mới
            bai_viet.anh = request.FILES['anh']

        # Lưu bài viết
        bai_viet.save()

        messages.success(request, "Bài viết đã được cập nhật thành công!")
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


@require_POST
def xoa_baiviet(request, bai_viet_id):
    try:
        # Tìm bài viết theo ma_bv
        bai_viet = get_object_or_404(BaiViet, ma_bv=bai_viet_id)

        # Xóa ảnh đại diện nếu có
        if bai_viet.anh:
            if os.path.isfile(bai_viet.anh.path):
                os.remove(bai_viet.anh.path)

        # Xóa bài viết
        tieu_de = bai_viet.tieu_de
        bai_viet.delete()

        # Trả về kết quả
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Đã xóa bài viết "{tieu_de}" thành công!'
            })

        messages.success(request, f'Đã xóa bài viết "{tieu_de}" thành công!')
        return redirect('quanlybaiviet')

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }, status=500)

        messages.error(request, f'Lỗi: {str(e)}')
        return redirect('quanlybaiviet')


def get_content(request, target):
    if target == 'quanlybaiviet':
        return quanlybaiviet(request)
    elif target.startswith('quanlybaiviet/thembaiviet'):
        return them_baiviet(request)
    elif target.startswith('quanlybaiviet/xembaiviet/'):
        try:
            bai_viet_id = int(target.split('/')[-1])
            return xem_baiviet(request, bai_viet_id)
        except (ValueError, IndexError):
            return HttpResponse("ID bài viết không hợp lệ", status=400)
    elif target.startswith('quanlybaiviet/suabaiviet/'):
        try:
            bai_viet_id = int(target.split('/')[-1])
            return sua_baiviet(request, bai_viet_id)
        except (ValueError, IndexError):
            return HttpResponse("ID bài viết không hợp lệ", status=400)
    else:
        return HttpResponse(f"Không tìm thấy nội dung cho {target}", status=404)

