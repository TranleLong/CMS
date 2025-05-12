from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from csdl.models import Menu, BaiViet
from .forms import MenuForm
from datetime import datetime


def quanlymenu(request):
    # Lấy danh sách menu
    menu_list = Menu.objects.all().order_by('-ngay_tao')

    # Tìm kiếm menu nếu có
    search_query = request.GET.get('search', '')
    if search_query:
        menu_list = menu_list.filter(
            Q(tieu_de__icontains=search_query) |
            Q(duong_dan__icontains=search_query)
        )

    context = {
        'menu_list': menu_list,
        'search_query': search_query,
    }

    return render(request, 'quanlymenu.html', context)


def them_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            # Lưu menu
            menu = form.save(commit=False)
            menu.ngay_tao = datetime.now().date()
            menu.save()

            # Lấy danh sách bài viết được chọn
            bai_viet_ids = request.POST.getlist('bai_viet_ids')
            if bai_viet_ids:
                # Cập nhật menu cho các bài viết được chọn
                BaiViet.objects.filter(ma_bv__in=bai_viet_ids).update(menu=menu)

            messages.success(request, "Menu đã được thêm thành công!")
            return redirect('quanlymenu')
    else:
        form = MenuForm()

    # Lấy danh sách bài viết để hiển thị trong form
    bai_viet_list = BaiViet.objects.all().order_by('-ngay_dang')

    context = {
        'form': form,
        'bai_viet_list': bai_viet_list,
    }

    return render(request, 'themmenu.html', context)


def xem_menu(request, menu_id):
    # Lấy thông tin menu
    menu = get_object_or_404(Menu, ma_menu=menu_id)

    # Lấy danh sách bài viết thuộc menu
    bai_viet_list = BaiViet.objects.filter(menu=menu).order_by('-ngay_dang')

    context = {
        'menu': menu,
        'bai_viet_list': bai_viet_list,
    }

    return render(request, 'xemmenu.html', context)


def sua_menu(request, menu_id):
    # Lấy thông tin menu
    menu = get_object_or_404(Menu, ma_menu=menu_id)

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            # Lưu menu
            menu = form.save()

            # Xóa liên kết menu cũ
            BaiViet.objects.filter(menu=menu).update(menu=None)

            # Lấy danh sách bài viết được chọn
            bai_viet_ids = request.POST.getlist('bai_viet_ids')
            if bai_viet_ids:
                # Cập nhật menu cho các bài viết được chọn
                BaiViet.objects.filter(ma_bv__in=bai_viet_ids).update(menu=menu)

            messages.success(request, "Menu đã được cập nhật thành công!")
            return redirect('quanlymenu')
    else:
        form = MenuForm(instance=menu)

    # Lấy danh sách bài viết để hiển thị trong form
    bai_viet_list = BaiViet.objects.all().order_by('-ngay_dang')

    # Lấy danh sách bài viết đã được chọn
    selected_bai_viet_ids = list(BaiViet.objects.filter(menu=menu).values_list('ma_bv', flat=True))

    context = {
        'form': form,
        'menu': menu,
        'bai_viet_list': bai_viet_list,
        'selected_bai_viet_ids': selected_bai_viet_ids,
    }

    return render(request, 'suamenu.html', context)


@require_POST
def xoa_menu(request, menu_id):
    try:
        # Tìm menu theo ma_menu
        menu = get_object_or_404(Menu, ma_menu=menu_id)

        # Xóa liên kết menu với bài viết
        BaiViet.objects.filter(menu=menu).update(menu=None)

        # Xóa menu
        tieu_de = menu.tieu_de
        menu.delete()

        # Trả về kết quả
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Đã xóa menu "{tieu_de}" thành công!'
            })

        messages.success(request, f'Đã xóa menu "{tieu_de}" thành công!')
        return redirect('quanlymenu')

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Lỗi: {str(e)}'
            }, status=500)

        messages.error(request, f'Lỗi: {str(e)}')
        return redirect('quanlymenu')


# Trang xem trước menu cho nhân viên
def xem_truoc_menu(request, menu_id):
    # Lấy thông tin menu
    menu = get_object_or_404(Menu, ma_menu=menu_id)

    # Lấy danh sách bài viết thuộc menu
    bai_viet_list = BaiViet.objects.filter(menu=menu).order_by('-ngay_dang')

    context = {
        'menu': menu,
        'bai_viet_list': bai_viet_list,
    }

    return render(request, 'xemtruocmenu.html', context)
