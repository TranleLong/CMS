from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password


# Hiển thị danh sách thành viên
def quanlythanhvien(request):
    # Lấy tất cả thành viên từ cơ sở dữ liệu
    thanh_vien_list = User.objects.all().order_by('username')

    # Truyền danh sách thành viên vào template
    context = {
        'thanh_vien_list': thanh_vien_list,
    }

    # Xử lý request AJAX (nếu có)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('quanlythanhvien.html', context, request=request)
        return HttpResponse(html)

    return render(request, 'quanlythanhvien.html', context)


# Thêm thành viên mới
def them_thanh_vien(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        vai_tro = request.POST.get('vai_tro')
        is_active = request.POST.get('is_active') == 'on'

        # Kiểm tra dữ liệu
        if not username or not password:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin thành viên.")
            return render(request, 'themthanhvien.html')

        # Kiểm tra username đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác.")
            return render(request, 'themthanhvien.html')

        # Tạo user mới
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),  # Mã hóa mật khẩu
            is_active=is_active,
            is_staff=(vai_tro == 'quan_ly')  # Nếu vai trò là quản lý thì is_staff = True
        )

        # Lưu user
        user.save()

        messages.success(request, "Thành viên đã được thêm thành công!")
        return redirect('quanlythanhvien')

    context = {
        'vai_tro_choices': [('nhan_vien', 'Nhân viên'), ('quan_ly', 'Quản lý')]
    }
    return render(request, 'themthanhvien.html', context)


# Xem chi tiết thành viên
def xem_thanh_vien(request, user_id):
    # Lấy thông tin thành viên từ cơ sở dữ liệu
    thanh_vien = get_object_or_404(User, id=user_id)

    context = {
        'thanh_vien': thanh_vien,
    }
    return render(request, 'xemthanhvien.html', context)


# Sửa thành viên
def sua_thanh_vien(request, user_id):
    # Lấy thông tin thành viên từ cơ sở dữ liệu
    thanh_vien = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        vai_tro = request.POST.get('vai_tro')
        is_active = request.POST.get('is_active') == 'on'

        # Kiểm tra dữ liệu
        if not username:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin thành viên.")
            return render(request, 'suathanhvien.html', {'thanh_vien': thanh_vien})

        # Kiểm tra username đã tồn tại chưa (trừ user hiện tại)
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác.")
            return render(request, 'suathanhvien.html', {'thanh_vien': thanh_vien})

        # Cập nhật thông tin cơ bản
        thanh_vien.username = username
        thanh_vien.email = email
        thanh_vien.first_name = first_name
        thanh_vien.last_name = last_name
        thanh_vien.is_active = is_active
        thanh_vien.is_staff = (vai_tro == 'quan_ly')

        # Cập nhật mật khẩu nếu có
        if password:
            thanh_vien.password = make_password(password)

        # Lưu thành viên
        thanh_vien.save()

        messages.success(request, "Thành viên đã được cập nhật thành công!")
        return redirect('quanlythanhvien')

    # Xác định vai trò hiện tại
    vai_tro = 'quan_ly' if thanh_vien.is_staff else 'nhan_vien'

    context = {
        'thanh_vien': thanh_vien,
        'vai_tro': vai_tro,
        'vai_tro_choices': [('nhan_vien', 'Nhân viên'), ('quan_ly', 'Quản lý')]
    }
    return render(request, 'suathanhvien.html', context)


# Xóa thành viên
@require_POST
def xoa_thanh_vien(request, user_id):
    try:
        # Tìm thành viên theo id
        thanh_vien = get_object_or_404(User, id=user_id)

        # Kiểm tra xem có phải là superuser không
        if thanh_vien.is_superuser:
            return JsonResponse({
                'success': False,
                'message': 'Không thể xóa tài khoản quản trị viên hệ thống.'
            })

        # Xóa thành viên
        username = thanh_vien.username
        thanh_vien.delete()
        return JsonResponse({'success': True, 'message': f'Thành viên {username} đã được xóa thành công!'})

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Thành viên không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Lỗi: {str(e)}'}, status=500)


# Hàm để lấy nội dung cho các trang khác
def get_content(request, target):
    if target == 'quanlythanhvien':
        return quanlythanhvien(request)
    elif target == 'quanlythanhvien/themthanhvien':
        return them_thanh_vien(request)
    elif target.startswith('quanlythanhvien/xemthanhvien/'):
        try:
            user_id = int(target.split('/')[-1])
            return xem_thanh_vien(request, user_id)
        except (ValueError, IndexError):
            return HttpResponse("ID thành viên không hợp lệ", status=400)
    elif target.startswith('quanlythanhvien/suathanhvien/'):
        try:
            user_id = int(target.split('/')[-1])
            return sua_thanh_vien(request, user_id)
        except (ValueError, IndexError):
            return HttpResponse("ID thành viên không hợp lệ", status=400)
    else:
        return HttpResponse(f"Không tìm thấy nội dung cho {target}", status=404)
