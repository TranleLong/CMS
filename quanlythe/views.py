from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from csdl.models import The, BaiViet
from django.template.loader import render_to_string


# Hiển thị danh sách thẻ
def quanlythe(request):
    # Lấy tất cả thẻ từ cơ sở dữ liệu
    the_list = The.objects.all().order_by('ten_the')

    # Truyền danh sách thẻ vào template
    context = {
        'the_list': the_list,
    }

    # Xử lý request AJAX (nếu có)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('quanlythe.html', context, request=request)
        return HttpResponse(html)

    return render(request, 'quanlythe.html', context)


# Thêm thẻ mới
def them_the(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ten_the = request.POST.get('ten_the')
        slug = request.POST.get('slug')
        mo_ta = request.POST.get('mo_ta')

        # Kiểm tra dữ liệu
        if not ten_the or not slug:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin thẻ.")
            return render(request, 'themthe.html')

        # Kiểm tra xem slug đã tồn tại chưa
        if The.objects.filter(slug=slug).exists():
            messages.error(request, "Đường dẫn (slug) đã tồn tại. Vui lòng chọn đường dẫn khác.")
            return render(request, 'themthe.html', {'ten_the': ten_the, 'mo_ta': mo_ta})

        # Tạo đối tượng thẻ mới
        the = The(
            ten_the=ten_the,
            slug=slug,
            mo_ta=mo_ta,
            so_bai_viet=0  # Mặc định số bài viết là 0
        )

        # Lưu thẻ
        the.save()

        messages.success(request, "Thẻ đã được thêm thành công!")
        return redirect('quanlythe')

    return render(request, 'themthe.html')


# Xem chi tiết thẻ
def xem_the(request, tag_id):
    # Lấy thông tin thẻ
    the = get_object_or_404(The, ma_the=tag_id)

    # Lấy danh sách bài viết thuộc thẻ này
    bai_viet_list = BaiViet.objects.filter(ma_the=the).order_by('-ngay_dang')[:10]  # Lấy 10 bài viết mới nhất

    context = {
        'the': the,
        'bai_viet_list': bai_viet_list,
    }

    return render(request, 'xemthe.html', context)


# Sửa thẻ
def sua_the(request, tag_id):
    # Lấy thông tin thẻ từ cơ sở dữ liệu
    the = get_object_or_404(The, ma_the=tag_id)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ten_the = request.POST.get('ten_the')
        slug = request.POST.get('slug')
        mo_ta = request.POST.get('mo_ta')

        # Kiểm tra dữ liệu
        if not ten_the or not slug:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin thẻ.")
            return render(request, 'suathe.html', {'the': the})

        # Kiểm tra xem slug đã tồn tại chưa (trừ thẻ hiện tại)
        if The.objects.filter(slug=slug).exclude(ma_the=tag_id).exists():
            messages.error(request, "Đường dẫn (slug) đã tồn tại. Vui lòng chọn đường dẫn khác.")
            return render(request, 'suathe.html', {'the': the})

        # Cập nhật thông tin thẻ
        the.ten_the = ten_the
        the.slug = slug
        the.mo_ta = mo_ta

        # Lưu thẻ
        the.save()

        messages.success(request, "Thẻ đã được cập nhật thành công!")
        return redirect('quanlythe')

    context = {
        'the': the,
    }
    return render(request, 'suathe.html', context)


# Xóa thẻ
@require_POST
def xoa_the(request, tag_id):
    try:
        # Tìm thẻ theo ma_the
        the = get_object_or_404(The, ma_the=tag_id)

        # Kiểm tra xem thẻ có bài viết không
        if the.so_bai_viet > 0:
            return JsonResponse({
                'success': False,
                'message': 'Không thể xóa thẻ này vì có bài viết. Vui lòng xóa bài viết trước hoặc gỡ thẻ khỏi bài viết.'
            })

        # Xóa thẻ
        the.delete()
        return JsonResponse({'success': True, 'message': 'Thẻ đã được xóa thành công!'})

    except The.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Thẻ không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'}, status=500)

# # Hàm để lấy nội dung cho các trang khác
# def get_content(request, target):
#     if target == 'quanlythe':
#         return quanlythe(request)
#     elif target == 'quanlythe/themthe':
#         return them_the(request)
#     elif target.startswith('quanlythe/xemthe/'):
#         try:
#             tag_id = int(target.split('/')[-1])
#             return xem_the(request, tag_id)
#         except (ValueError, IndexError):
#             return HttpResponse("ID thẻ không hợp lệ", status=400)
#     elif target.startswith('quanlythe/suathe/'):
#         try:
#             tag_id = int(target.split('/')[-1])
#             return sua_the(request, tag_id)
#         except (ValueError, IndexError):
#             return HttpResponse("ID thẻ không hợp lệ", status=400)
#     elif target.startswith('quanlythe/xoathe/'):
#         try:
#             tag_id = int(target.split('/')[-1])
#             return xoa_the(request, tag_id)
#         except (ValueError, IndexError):
#             return HttpResponse("ID thẻ không hợp lệ", status=400)
#     else:
#         return HttpResponse(f"Không tìm thấy nội dung cho {target}", status=404)
