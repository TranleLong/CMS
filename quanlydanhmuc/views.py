from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from csdl.models import DanhMuc, BaiViet
from .forms import DanhMucForm

@login_required(login_url='login')
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
