from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.db import transaction, connection

from csdl.models import Menu, BaiViet, MenuBaiViet, DanhMuc
import json
import logging

# Thiết lập logging
logger = logging.getLogger(__name__)

from quanlymenu.forms import MenuForm


@login_required(login_url='login')
def quanlymenu(request):
    menu_list = Menu.objects.all().order_by('thu_tu')

    # Thêm số lượng bài viết cho mỗi menu
    for menu in menu_list:
        if menu.loai_menu == 'bai_viet':
            # Đếm số lượng bài viết trong menu
            menu.bai_viet_count = MenuBaiViet.objects.filter(ma_menu_id=menu.ma_menu).count()
        else:
            menu.bai_viet_count = 0

    return render(request, 'quanlymenu.html', {'menu_list': menu_list})


@login_required(login_url='login')
@transaction.atomic
def them_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            # Lưu menu
            menu = form.save(commit=False)
            menu.thu_tu = request.POST.get('thu_tu', 0)

            # Xử lý loại menu
            loai_menu = request.POST.get('loai_menu')
            menu.loai_menu = loai_menu

            if loai_menu == 'duong_dan':
                # Nếu là menu đường dẫn, lưu URL
                menu.url = form.cleaned_data['url']

            # Lưu menu trước khi tạo quan hệ với bài viết
            menu.save()

            # Nếu là menu bài viết, xử lý bài viết được chọn
            if loai_menu == 'bai_viet':
                bai_viet_ids = request.POST.getlist('bai_viet_ids')

                if bai_viet_ids:
                    # Tạo các bản ghi trong bảng MenuBaiViet
                    for i, bv_id in enumerate(bai_viet_ids):
                        try:
                            bai_viet = BaiViet.objects.get(ma_bv=bv_id)

                            # Sử dụng SQL trực tiếp để chắc chắn dữ liệu được lưu đúng
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO csdl_baiviet_menu (ma_menu_id, ma_bv_id, thu_tu) VALUES (%s, %s, %s)",
                                    [menu.ma_menu, bai_viet.ma_bv, i]
                                )

                        except BaiViet.DoesNotExist:
                            pass
                        except Exception as e:
                            pass

            messages.success(request, 'Thêm menu thành công!')
            return redirect('quanlymenu')
    else:
        form = MenuForm()

    bai_viet_list = BaiViet.objects.all().order_by('-ngay_dang')

    return render(request, 'themmenu.html', {
        'form': form,
        'bai_viet_list': bai_viet_list
    })


@login_required(login_url='login')
@transaction.atomic
def sua_menu(request, menu_id):
    menu = get_object_or_404(Menu, ma_menu=menu_id)

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            # Lưu menu
            menu = form.save(commit=False)
            menu.thu_tu = request.POST.get('thu_tu', 0)

            # Xử lý loại menu
            loai_menu = request.POST.get('loai_menu')
            menu.loai_menu = loai_menu

            if loai_menu == 'duong_dan':
                # Nếu là menu đường dẫn, lưu URL
                menu.url = form.cleaned_data['url']
            else:
                # Nếu chuyển từ đường dẫn sang bài viết, xóa URL
                menu.url = None

            # Lưu menu trước khi cập nhật quan hệ với bài viết
            menu.save()

            # Xóa tất cả liên kết bài viết hiện tại từ bảng csdl_baiviet_menu
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM csdl_baiviet_menu WHERE ma_menu_id = %s", [menu.ma_menu])

            # Nếu là menu bài viết, xử lý bài viết được chọn
            if loai_menu == 'bai_viet':
                bai_viet_ids = request.POST.getlist('bai_viet_ids')

                if bai_viet_ids:
                    # Tạo các bản ghi trong bảng csdl_baiviet_menu
                    for i, bv_id in enumerate(bai_viet_ids):
                        try:
                            bai_viet = BaiViet.objects.get(ma_bv=bv_id)

                            # Sử dụng SQL trực tiếp để chắc chắn dữ liệu được lưu đúng
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO csdl_baiviet_menu (ma_menu_id, ma_bv_id, thu_tu) VALUES (%s, %s, %s)",
                                    [menu.ma_menu, bai_viet.ma_bv, i]
                                )

                        except BaiViet.DoesNotExist:
                            pass
                        except Exception as e:
                            pass

            messages.success(request, 'Cập nhật menu thành công!')
            return redirect('quanlymenu')
    else:
        form = MenuForm(instance=menu)

    bai_viet_list = BaiViet.objects.all().order_by('-ngay_dang')

    # Lấy danh sách ID bài viết đã chọn từ bảng csdl_baiviet_menu
    with connection.cursor() as cursor:
        cursor.execute("SELECT ma_bv_id FROM csdl_baiviet_menu WHERE ma_menu_id = %s", [menu.ma_menu])
        selected_bai_viet_ids = [row[0] for row in cursor.fetchall()]

    return render(request, 'suamenu.html', {
        'form': form,
        'menu': menu,
        'bai_viet_list': bai_viet_list,
        'selected_bai_viet_ids': selected_bai_viet_ids
    })


@login_required(login_url='login')
def xem_menu(request, menu_id):
    menu = get_object_or_404(Menu, ma_menu=menu_id)

    if menu.loai_menu == 'bai_viet':
        try:
            # Lấy bài viết từ bảng csdl_baiviet_menu
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT b.* FROM csdl_baiviet b
                    JOIN csdl_baiviet_menu bm ON b.ma_bv = bm.ma_bv_id
                    WHERE bm.ma_menu_id = %s
                    ORDER BY bm.thu_tu
                """, [menu.ma_menu])
                columns = [col[0] for col in cursor.description]
                bai_viet_list = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            # Chuyển đổi từ dict sang đối tượng BaiViet
            for i, bv_dict in enumerate(bai_viet_list):
                bai_viet = BaiViet()
                for key, value in bv_dict.items():
                    setattr(bai_viet, key, value)
                bai_viet_list[i] = bai_viet

            # Thêm thông tin trạng thái cho mỗi bài viết
            for bai_viet in bai_viet_list:
                if bai_viet.trang_thai == 'Đã duyệt':
                    bai_viet.visible_in_menu = True
                else:
                    bai_viet.visible_in_menu = False

        except Exception as e:
            bai_viet_list = []
    else:
        bai_viet_list = []

    return render(request, 'xemmenu.html', {
        'menu': menu,
        'bai_viet_list': bai_viet_list
    })


@login_required(login_url='login')
def xem_truoc_menu(request, menu_id):
    menu = get_object_or_404(Menu, ma_menu=menu_id)

    if menu.loai_menu == 'bai_viet':
        try:
            # Lấy bài viết từ bảng csdl_baiviet_menu
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT b.* FROM csdl_baiviet b
                    JOIN csdl_baiviet_menu bm ON b.ma_bv = bm.ma_bv_id
                    WHERE bm.ma_menu_id = %s AND b.trang_thai = 'Đã duyệt'
                    ORDER BY bm.thu_tu
                """, [menu.ma_menu])
                columns = [col[0] for col in cursor.description]
                bai_viet_list = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            # Chuyển đổi từ dict sang đối tượng BaiViet
            for i, bv_dict in enumerate(bai_viet_list):
                bai_viet = BaiViet()
                for key, value in bv_dict.items():
                    setattr(bai_viet, key, value)
                bai_viet_list[i] = bai_viet

        except Exception as e:
            bai_viet_list = []
    else:
        bai_viet_list = []

    return render(request, 'menu.html', {
        'menu': menu,
        'bai_viet_list': bai_viet_list
    })


@login_required(login_url='login')
def xoa_menu(request, menu_id):
    if request.method == 'POST':
        menu = get_object_or_404(Menu, ma_menu=menu_id)

        try:
            # Xóa các liên kết csdl_baiviet_menu trước
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM csdl_baiviet_menu WHERE ma_menu_id = %s", [menu.ma_menu])

            # Xóa menu
            menu.delete()
            return JsonResponse({'success': True, 'message': 'Xóa menu thành công!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Lỗi khi xóa menu: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Phương thức không được hỗ trợ'})


# Thêm hàm để lấy menu cho header
def get_header_menus():
    """
    Lấy danh sách menu cho header
    """
    try:
        # Lấy các menu đang hoạt động và sắp xếp theo thứ tự
        menus = Menu.objects.filter(trang_thai='Dang hoat dong').order_by('thu_tu')

        # Với mỗi menu loại bài viết, lấy danh sách bài viết
        for menu in menus:
            if menu.loai_menu == 'bai_viet':
                try:
                    # Lấy danh sách bài viết đã duyệt liên quan đến menu này
                    menu_bai_viet = MenuBaiViet.objects.filter(ma_menu=menu)

                    bai_viet_ids = menu_bai_viet.values_list('ma_bv', flat=True)

                    # Lấy bài viết đã duyệt
                    articles = BaiViet.objects.filter(
                        ma_bv__in=bai_viet_ids,
                        trang_thai='Đã duyệt'
                    )

                    for article in articles:
                        # Lưu đường dẫn gốc
                        article.original_path = article.duong_dan

                        # Chuẩn hóa đường dẫn
                        if article.duong_dan:
                            # Loại bỏ dấu / ở đầu và cuối
                            if article.duong_dan.startswith('/'):
                                article.duong_dan = article.duong_dan[1:]
                            if article.duong_dan.endswith('/'):
                                article.duong_dan = article.duong_dan[:-1]
                            # Loại bỏ http:// hoặc https:// nếu có
                            if article.duong_dan.startswith('http://'):
                                article.duong_dan = article.duong_dan[7:]
                            if article.duong_dan.startswith('https://'):
                                article.duong_dan = article.duong_dan[8:]
                            # Loại bỏ tên miền nếu có
                            if '/' in article.duong_dan and not article.duong_dan.startswith('bai-viet/'):
                                parts = article.duong_dan.split('/', 1)
                                if len(parts) > 1:
                                    article.duong_dan = parts[1]
                            # Loại bỏ tiền tố bai-viet/ nếu có
                            if article.duong_dan.startswith('bai-viet/'):
                                article.duong_dan = article.duong_dan[9:]

                    # Gán danh sách bài viết vào menu
                    menu.articles = articles

                    # Chuyển đổi QuerySet thành list để tránh lỗi khi gọi count()
                    if hasattr(menu, 'articles'):
                        menu.articles = list(menu.articles)

                except Exception as e:
                    menu.articles = []
            else:
                menu.articles = []

        return menus
    except Exception as e:
        return []
