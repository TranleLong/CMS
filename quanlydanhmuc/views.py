# from django.contrib import messages
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.template.loader import render_to_string
# from django.views.decorators.http import require_POST
# from csdl.models import DanhMuc
# from .forms import DanhMucForm
# # Create your views here.
# def quanlydanhmuc(request):
#     # Thêm debug để kiểm tra model và giá trị target
#     # print(f"DEBUG: Target = {target}")
#     print("DEBUG: Model DanhMuc:", DanhMuc)
#
#     # Lấy tất cả danh mục
#     danh_mucs = DanhMuc.objects.all()
#
#     # In ra từng danh mục để kiểm tra
#     for dm in danh_mucs:
#         print(f"DEBUG: Danh mục: ID={dm.ma_dm}, Tên={dm.ten_dm}, Slug={dm.slug}")
#
#     # Truyền danh sách danh mục vào template
#     context = {
#         'danh_muc_tree': danh_mucs,  # Sử dụng tên biến này để khớp với template
#     }
#
#     return render(request, 'quanlydanhmuc.html', context)
# # def get_content(request, target):
# #     print(f"DEBUG: target = {target}")  # In ra giá trị của target để kiểm tra
# #     if target == 'quanlybaiviet':
# #         # Trả về nội dung block bài viết
# #         context = {
# #             'baiviet_data': 'Nội dung bài viết mặc định'
# #         }
# #         return render(request, 'quanlybaiviet.html', context)
# #     elif target == 'quanlydanhmuc':
# #         print("DEBUG: Model DanhMuc:", DanhMuc)
# #         # Lấy tất cả danh mục từ model DanhMuc và sắp xếp theo 'order_index'
# #         danh_mucs = DanhMuc.objects.all().order_by('order_index')
# #         # Kiểm tra số lượng danh mục
# #         print(f"DEBUG: Số lượng danh mục: {danh_mucs.count()}")
# #
# #         # In ra từng danh mục để kiểm tra
# #         for dm in danh_mucs:
# #             print(f"DEBUG: Danh mục: ID={dm.ma_dm}, Tên={dm.ten_dm}, Slug={dm.slug}")
# #
# #         # Truyền danh sách danh mục vào template
# #         context = {
# #             'danh_muc_tree': danh_mucs,  # Truyền danh sách danh mục vào template
# #         }
# #
# #         # Kiểm tra nếu là request AJAX
# #         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
# #             from django.template.loader import render_to_string
# #             html = render_to_string('quanlydanhmuc.html', context, request=request)
# #             return HttpResponse(html)
# #
# #         # Render lại trang nếu không phải request AJAX
# #         return render(request, 'quanlydanhmuc.html', context)
# #
# #     elif target == 'dashboard':
# #         context = {
# #             'dashboard_data': 'Nội dung dashboard'
# #         }
# #         return render(request, 'dashboard.html', context)
# #     elif target == 'quanlythe':
# #         context = {
# #             'the_data': 'Nội dung quanlythe'
# #         }
# #         return render(request, 'quanlythe.html', context)
# #     elif target == 'quanlymedia':
# #         context = {
# #             'media_data': 'Nội dung quanlymedia'
# #         }
# #         return render(request, 'quanlymedia.html', context)
# #     elif target == 'quanlythanhvien':
# #         context = {
# #             'thanhvien_data': 'Nội dung quanlythanhvien'
# #         }
# #         return render(request, 'quanlythanhvien.html', context)
# #     elif target == 'quanlycauhinh':
# #         context = {
# #             'cauhinh_data': 'Nội dung quanlycauhinh'
# #         }
# #         return render(request, 'quanlycauhinh.html', context)
# #     elif target == 'quanlymenu':
# #         context = {
# #             'quanlymenu_data': 'Nội dung menu'
# #         }
# #         return render(request, 'quanlymenu.html', context)
#
# def them_danhmuc(request):
#     if request.method == 'POST':
#         category_name = request.POST.get('categoryName')
#         category_slug = request.POST.get('categorySlug')
#         category_description = request.POST.get('categoryDescription')
#         parent_category = request.POST.get('parentCategory')
#         status = request.POST.get('status')
#
#         # Kiểm tra xem thông tin có đầy đủ không
#         if not category_name or not category_slug:
#             messages.error(request, "Vui lòng nhập đầy đủ thông tin danh mục.")
#             return render(request, 'themdanhmuc.html')
#
#         # Xử lý để lấy đối tượng danh mục cha (nếu có)
#         parent_category_obj = None
#         if parent_category:
#             parent_category_obj = DanhMuc.objects.get(id=parent_category)
#
#         # Tạo danh mục mới
#         new_category = DanhMuc(
#             ten_dm=category_name,
#             slug=category_slug,
#             mo_ta=category_description,
#             parent_id=parent_category_obj,
#             trang_thai=status == 'on',  # Chuyển trạng thái thành True hoặc False
#             order_index=1  # Có thể tự động tính số thứ tự hoặc nhập từ form nếu cần
#         )
#         new_category.save()
#
#         messages.success(request, "Danh mục đã được thêm thành công!")
#         return redirect('quanlydanhmuc')  # Điều hướng về trang quản lý danh mục
#
#     # Render lại trang nếu không phải POST
#     return render(request, 'themdanhmuc.html')
# def xem_danhmuc(request, category_id):
#     # Giả sử bạn sẽ lấy dữ liệu theo category_id từ cơ sở dữ liệu
#     context = {
#         'category_id': category_id,
#         'category_data': f'Nội dung danh mục với ID {category_id}'  # Bạn có thể thay thế bằng dữ liệu thực tế từ DB
#     }
#     return render(request, 'xemdanhmuc.html', context)
# def sua_danhmuc(request, category_id):
#     # Giả sử bạn sẽ lấy dữ liệu theo category_id từ cơ sở dữ liệu
#     context = {
#         'category_id': category_id,
#         'category_data': f'Nội dung danh mục với ID {category_id}'  # Bạn có thể thay thế bằng dữ liệu thực tế từ DB
#     }
#     return render(request, 'suadanhmuc.html', context)
#
# @require_POST
# def xoa_danhmuc(request, category_id):
#     try:
#         # Tìm danh mục theo ma_dm (không phải id)
#         danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)
#
#         # Kiểm tra xem danh mục có danh mục con không
#         if DanhMuc.objects.filter(parent_id=danh_muc).exists():
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Không thể xóa danh mục này vì có danh mục con. Vui lòng xóa danh mục con trước.'
#             })
#
#         # Kiểm tra xem danh mục có bài viết không
#         if danh_muc.so_bai_viet > 0:
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Không thể xóa danh mục này vì có bài viết. Vui lòng xóa bài viết trước hoặc chuyển bài viết sang danh mục khác.'
#             })
#
#         # Xóa danh mục
#         danh_muc.delete()
#         return JsonResponse({'success': True, 'message': 'Danh mục đã được xóa thành công!'})
#
#     except DanhMuc.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'Danh mục không tồn tại'}, status=404)
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'}, status=500)
#
#
# # from django.contrib import messages
# # from django.http import HttpResponse, JsonResponse
# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.template.loader import render_to_string
# # from django.views.decorators.http import require_POST
# # from csdl.models import DanhMuc
# # from .forms import DanhMucForm
# #
# #
# # # Create your views here.
# # def quanlydanhmuc(request):
# #     # Lấy tất cả danh mục
# #     danh_mucs = DanhMuc.objects.all().order_by('order_index')
# #
# #     # In ra từng danh mục để kiểm tra
# #     for dm in danh_mucs:
# #         print(f"DEBUG: Danh mục: ID={dm.ma_dm}, Tên={dm.ten_dm}, Slug={dm.slug}")
# #
# #     # Tạo dictionary để lưu trữ danh mục con
# #     danh_muc_children = {}
# #
# #     # Lấy tất cả danh mục cha (parent_id is None)
# #     danh_muc_cha = danh_mucs.filter(parent_id__isnull=True)
# #
# #     # Lấy danh mục con cho mỗi danh mục cha
# #     for dm in danh_muc_cha:
# #         children = danh_mucs.filter(parent_id=dm)
# #         if children.exists():
# #             danh_muc_children[dm.ma_dm] = children
# #
# #     # Truyền danh sách danh mục vào template
# #     context = {
# #         'danh_muc_tree': danh_muc_cha,  # Chỉ truyền danh mục cha
# #         'danh_muc_children': danh_muc_children,  # Truyền từ điển danh mục con
# #     }
# #
# #     return render(request, 'quanlydanhmuc.html', context)
# #
# #
# # def them_danhmuc(request):
# #     if request.method == 'POST':
# #         form = DanhMucForm(request.POST)
# #         if form.is_valid():
# #             danh_muc = form.save(commit=False)
# #
# #             # Xử lý trường order_index tự động
# #             if DanhMuc.objects.exists():
# #                 max_order = DanhMuc.objects.all().order_by('-order_index').first().order_index
# #                 danh_muc.order_index = max_order + 1
# #             else:
# #                 danh_muc.order_index = 1
# #
# #             danh_muc.so_bai_viet = 0  # Mặc định là 0 bài viết
# #             danh_muc.save()
# #
# #             messages.success(request, "Danh mục đã được thêm thành công!")
# #             return redirect('quanlydanhmuc')
# #     else:
# #         form = DanhMucForm()
# #
# #     context = {
# #         'form': form,
# #         'parent_categories': DanhMuc.objects.filter(parent_id__isnull=True),
# #     }
# #     return render(request, 'themdanhmuc.html', context)
# #
# #
# # def xem_danhmuc(request, category_id):
# #     danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)
# #     so_bai_viet = danh_muc.so_bai_viet
# #     danh_muc_con = DanhMuc.objects.filter(parent_id=danh_muc)
# #
# #     context = {
# #         'danh_muc': danh_muc,
# #         'so_bai_viet': so_bai_viet,
# #         'danh_muc_con': danh_muc_con,
# #     }
# #     return render(request, 'xemdanhmuc.html', context)
# #
# #
# # def sua_danhmuc(request, category_id):
# #     danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)
# #
# #     if request.method == 'POST':
# #         form = DanhMucForm(request.POST, instance=danh_muc)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, "Danh mục đã được cập nhật thành công!")
# #             return redirect('quanlydanhmuc')
# #     else:
# #         form = DanhMucForm(instance=danh_muc)
# #
# #     # Loại bỏ danh mục hiện tại và các danh mục con của nó khỏi danh sách danh mục cha
# #     parent_categories = DanhMuc.objects.exclude(ma_dm=category_id)
# #     child_ids = get_all_child_ids(category_id)
# #     parent_categories = parent_categories.exclude(ma_dm__in=child_ids)
# #
# #     context = {
# #         'form': form,
# #         'danh_muc': danh_muc,
# #         'parent_categories': parent_categories,
# #     }
# #     return render(request, 'suadanhmuc.html', context)
# #
# #
# # @require_POST
# # def xoa_danhmuc(request, category_id):
# #     try:
# #         # Tìm danh mục theo ma_dm (không phải id)
# #         danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)
# #
# #         # Kiểm tra xem danh mục có danh mục con không
# #         if DanhMuc.objects.filter(parent_id=danh_muc).exists():
# #             return JsonResponse({
# #                 'success': False,
# #                 'message': 'Không thể xóa danh mục này vì có danh mục con. Vui lòng xóa danh mục con trước.'
# #             })
# #
# #         # Kiểm tra xem danh mục có bài viết không
# #         if danh_muc.so_bai_viet > 0:
# #             return JsonResponse({
# #                 'success': False,
# #                 'message': 'Không thể xóa danh mục này vì có bài viết. Vui lòng xóa bài viết trước hoặc chuyển bài viết sang danh mục khác.'
# #             })
# #
# #         # Xóa danh mục
# #         danh_muc.delete()
# #         return JsonResponse({'success': True, 'message': 'Danh mục đã được xóa thành công!'})
# #
# #     except DanhMuc.DoesNotExist:
# #         return JsonResponse({'success': False, 'message': 'Danh mục không tồn tại'}, status=404)
# #     except Exception as e:
# #         return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'}, status=500)
# #
#
# # # Hàm hỗ trợ để lấy tất cả ID của danh mục con
# # def get_all_child_ids(category_id):
# #     child_ids = []
# #     children = DanhMuc.objects.filter(parent_id=category_id)
# #
# #     for child in children:
# #         child_ids.append(child.ma_dm)
# #         child_ids.extend(get_all_child_ids(child.ma_dm))
# #
# #     return child_ids
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from csdl.models import DanhMuc, BaiViet
from .forms import DanhMucForm


# Create your views here.
def quanlydanhmuc(request):
    # Lấy tất cả danh mục
    danh_mucs = DanhMuc.objects.all().order_by('order_index')

    # Tạo dictionary để lưu trữ danh mục con
    danh_muc_children = {}

    # Lấy tất cả danh mục cha (parent_id is None)
    danh_muc_cha = danh_mucs.filter(parent_id__isnull=True)

    # Lấy danh mục con cho mỗi danh mục cha
    for dm in danh_muc_cha:
        children = danh_mucs.filter(parent_id=dm)
        if children.exists():
            danh_muc_children[dm.ma_dm] = children

    # Truyền danh sách danh mục vào template
    context = {
        'danh_muc_tree': danh_muc_cha,  # Chỉ truyền danh mục cha
        'danh_muc_children': danh_muc_children,  # Truyền từ điển danh mục con
    }

    return render(request, 'quanlydanhmuc.html', context)


def them_danhmuc(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ten_dm = request.POST.get('categoryName')
        slug = request.POST.get('categorySlug')
        mo_ta = request.POST.get('categoryDescription')
        parent_id = request.POST.get('parentCategory')
        trang_thai = request.POST.get('status') == 'on'

        # Kiểm tra dữ liệu
        if not ten_dm or not slug:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin danh mục.")
            parent_categories = DanhMuc.objects.all()
            return render(request, 'themdanhmuc.html', {'parent_categories': parent_categories})

        # Tạo đối tượng danh mục mới
        danh_muc = DanhMuc(
            ten_dm=ten_dm,
            slug=slug,
            mo_ta=mo_ta,
            trang_thai=trang_thai
        )

        # Xử lý danh mục cha nếu có
        if parent_id and parent_id.strip():
            try:
                parent = DanhMuc.objects.get(ma_dm=parent_id)
                danh_muc.parent_id = parent
            except DanhMuc.DoesNotExist:
                pass

        # Xử lý order_index
        if DanhMuc.objects.exists():
            max_order = DanhMuc.objects.all().order_by('-order_index').first().order_index
            danh_muc.order_index = max_order + 1
        else:
            danh_muc.order_index = 1

        # Mặc định số bài viết là 0
        danh_muc.so_bai_viet = 0

        # Lưu danh mục
        danh_muc.save()

        messages.success(request, "Danh mục đã được thêm thành công!")
        return redirect('quanlydanhmuc')

    # Lấy tất cả danh mục để hiển thị trong dropdown
    parent_categories = DanhMuc.objects.all()

    context = {
        'parent_categories': parent_categories,
    }
    return render(request, 'themdanhmuc.html', context)


def xem_danhmuc(request, category_id):
    # Lấy thông tin danh mục
    danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)

    # Lấy danh sách danh mục con
    danh_muc_con = DanhMuc.objects.filter(parent_id=danh_muc)

    # Lấy danh sách bài viết thuộc danh mục này
    bai_viet_list = BaiViet.objects.filter(ma_dm=danh_muc).order_by('-ngay_dang')[:10]  # Lấy 10 bài viết mới nhất

    context = {
        'danh_muc': danh_muc,
        'danh_muc_con': danh_muc_con,
        'bai_viet_list': bai_viet_list,
    }
    return render(request, 'xemdanhmuc.html', context)


def sua_danhmuc(request, category_id):
    danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ten_dm = request.POST.get('ten_dm')
        slug = request.POST.get('slug')
        mo_ta = request.POST.get('mo_ta')
        parent_id = request.POST.get('parent_id')
        trang_thai = request.POST.get('trang_thai') == 'on'

        # Kiểm tra dữ liệu
        if not ten_dm or not slug:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin danh mục.")
        else:
            # Cập nhật thông tin danh mục
            danh_muc.ten_dm = ten_dm
            danh_muc.slug = slug
            danh_muc.mo_ta = mo_ta
            danh_muc.trang_thai = trang_thai

            # Xử lý danh mục cha
            if parent_id:
                try:
                    parent = DanhMuc.objects.get(ma_dm=parent_id)
                    # Kiểm tra xem danh mục cha có phải là con của danh mục hiện tại không
                    child_ids = get_all_child_ids(category_id)
                    if int(parent_id) in child_ids or int(parent_id) == category_id:
                        messages.error(request, "Không thể chọn danh mục này làm danh mục cha.")
                        parent_categories = DanhMuc.objects.exclude(ma_dm=category_id).exclude(ma_dm__in=child_ids)
                        return render(request, 'suadanhmuc.html',
                                      {'danh_muc': danh_muc, 'parent_categories': parent_categories})
                    danh_muc.parent_id = parent
                except DanhMuc.DoesNotExist:
                    danh_muc.parent_id = None
            else:
                danh_muc.parent_id = None

            # Lưu danh mục
            danh_muc.save()
            messages.success(request, "Danh mục đã được cập nhật thành công!")
            return redirect('quanlydanhmuc')

    # Loại bỏ danh mục hiện tại và các danh mục con của nó khỏi danh sách danh mục cha
    parent_categories = DanhMuc.objects.exclude(ma_dm=category_id)
    child_ids = get_all_child_ids(category_id)
    parent_categories = parent_categories.exclude(ma_dm__in=child_ids)

    context = {
        'danh_muc': danh_muc,
        'parent_categories': parent_categories,
    }
    return render(request, 'suadanhmuc.html', context)


@require_POST
def xoa_danhmuc(request, category_id):
    try:
        # Tìm danh mục theo ma_dm
        danh_muc = get_object_or_404(DanhMuc, ma_dm=category_id)

        # Kiểm tra xem danh mục có bài viết không
        if danh_muc.so_bai_viet > 0:
            return JsonResponse({
                'success': False,
                'message': 'Không thể xóa danh mục này vì có bài viết. Vui lòng xóa bài viết trước hoặc chuyển bài viết sang danh mục khác.'
            })

        # Xóa danh mục
        danh_muc.delete()
        return JsonResponse({'success': True, 'message': 'Danh mục đã được xóa thành công!'})

    except DanhMuc.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Danh mục không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'}, status=500)


# Hàm hỗ trợ để lấy tất cả ID của danh mục con
def get_all_child_ids(category_id):
    child_ids = []
    children = DanhMuc.objects.filter(parent_id=category_id)

    for child in children:
        child_ids.append(child.ma_dm)
        child_ids.extend(get_all_child_ids(child.ma_dm))

    return child_ids
