from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from csdl.models import Media
from django.contrib.auth.models import User
from .forms import MediaForm
import os
import mimetypes
import zipfile
import io

@login_required(login_url='login')
def quanlymedia(request):
    # Lấy tham số từ URL
    folder = request.GET.get('folder', '')
    search_query = request.GET.get('search', '')

    # Lọc media theo thư mục và từ khóa tìm kiếm
    if folder:
        media_list = Media.objects.filter(folder_name=folder)
    else:
        media_list = Media.objects.all()

    if search_query:
        media_list = media_list.filter(
            Q(file_name__icontains=search_query) |
            Q(folder_name__icontains=search_query)
        )

    # Lấy danh sách các thư mục duy nhất
    folders = Media.objects.values_list('folder_name', flat=True).distinct()

    # Phân trang
    paginator = Paginator(media_list, 12)  # 12 items per page
    page_number = request.GET.get('page', 1)
    media_page = paginator.get_page(page_number)

    context = {
        'media_list': media_page,
        'folders': folders,
        'current_folder': folder,
        'search_query': search_query,
    }

    return render(request, 'quanlymedia.html', context)


def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            # Lấy thông tin từ form
            folder_name = form.cleaned_data['folder_name']
            uploaded_file = request.FILES['image']
            file_name = uploaded_file.name
            file_size = uploaded_file.size

            # Xác định loại file
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                type_name = 'image'
            elif file_extension in ['.mp4', '.avi', '.mov']:
                type_name = 'video'
            elif file_extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']:
                type_name = 'document'
            else:
                type_name = 'other'

            # Lấy user đầu tiên trong hệ thống hoặc tạo một user mặc định
            try:
                default_user = User.objects.first()
                if not default_user:
                    # Nếu không có user nào, tạo một user mặc định
                    default_user = User.objects.create_user(
                        username='default_user',
                        password='default_password',
                        email='default@example.com'
                    )
            except:
                # Nếu có lỗi, tạo một user mặc định
                default_user = User.objects.create_user(
                    username='default_user',
                    password='default_password',
                    email='default@example.com'
                )

            # Tạo media mới
            media = Media(
                folder_name=folder_name,
                file_name=file_name,
                type_name=type_name,
                size=file_size,
                image=uploaded_file,
                ma_nguoi_dung=default_user
            )
            media.save()

            # Trả về thành công nếu là AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Tải lên thành công!',
                    'media': {
                        'id': media.ma_media,
                        'name': media.file_name,
                        'type': media.type_name,
                        'size': media.size,
                        'url': media.image.url if media.image else '',
                    }
                })

            messages.success(request, 'Tải lên thành công!')
            return redirect('quanlymedia')
        else:
            # Trả về lỗi nếu là AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Lỗi khi tải lên file.',
                    'errors': form.errors
                })

            messages.error(request, 'Lỗi khi tải lên file.')
    else:
        form = MediaForm()

    context = {
        'form': form,
    }
    return render(request, 'upload_media.html', context)


def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name', '')

        if folder_name:
            # Kiểm tra xem thư mục đã tồn tại chưa
            if Media.objects.filter(folder_name=folder_name).exists():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Thư mục đã tồn tại!'
                    })
                messages.error(request, 'Thư mục đã tồn tại!')
            else:
                # Tạo thư mục mới (không cần tạo bản ghi trong DB vì thư mục chỉ là thuộc tính của media)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Tạo thư mục thành công!',
                        'folder': folder_name
                    })
                messages.success(request, 'Tạo thư mục thành công!')
                return redirect('quanlymedia')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Vui lòng nhập tên thư mục!'
                })
            messages.error(request, 'Vui lòng nhập tên thư mục!')

    return redirect('quanlymedia')


def view_media(request, media_id):
    media = get_object_or_404(Media, ma_media=media_id)

    # Nếu là AJAX request, trả về thông tin media dưới dạng JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'media': {
                'id': media.ma_media,
                'name': media.file_name,
                'folder': media.folder_name,
                'type': media.type_name,
                'size': media.size,
                'url': media.image.url if media.image else '',
                'date': media.image.name if media.image else '',
            }
        })

    context = {
        'media': media,
    }
    return render(request, 'view_media.html', context)


def download_media(request, media_id):
    media = get_object_or_404(Media, ma_media=media_id)

    if media.image:
        file_path = media.image.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = f'attachment; filename={media.file_name}'
                return response

    # Nếu file không tồn tại hoặc không có file
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': 'Không thể tải xuống file!'
        })

    messages.error(request, 'Không thể tải xuống file!')
    return redirect('quanlymedia')


def download_folder(request, folder_name):
    # Lấy tất cả media trong thư mục
    media_list = Media.objects.filter(folder_name=folder_name)

    if not media_list.exists():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Thư mục trống hoặc không tồn tại!'
            })
        messages.error(request, 'Thư mục trống hoặc không tồn tại!')
        return redirect('quanlymedia')

    # Tạo file ZIP
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for media in media_list:
            if media.image:
                file_path = media.image.path
                if os.path.exists(file_path):
                    # Thêm file vào ZIP
                    zip_file.write(file_path, media.file_name)

    # Trả về file ZIP
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={folder_name}.zip'
    return response


@require_POST
def delete_media(request, media_id):
    media = get_object_or_404(Media, ma_media=media_id)

    # Xóa file từ hệ thống file
    if media.image:
        if os.path.exists(media.image.path):
            os.remove(media.image.path)

    # Xóa bản ghi từ database
    media.delete()

    # Trả về kết quả
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Xóa file thành công!'
        })

    messages.success(request, 'Xóa file thành công!')
    return redirect('quanlymedia')


@require_POST
def delete_folder(request, folder_name):
    # Lấy tất cả media trong thư mục
    media_list = Media.objects.filter(folder_name=folder_name)

    # Xóa từng file trong thư mục
    for media in media_list:
        if media.image:
            if os.path.exists(media.image.path):
                os.remove(media.image.path)
        media.delete()

    # Trả về kết quả
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Đã xóa thư mục "{folder_name}" thành công!'
        })

    messages.success(request, f'Đã xóa thư mục "{folder_name}" thành công!')
    return redirect('quanlymedia')


def get_folders(request):
    # Lấy danh sách các thư mục duy nhất
    folders = Media.objects.values_list('folder_name', flat=True).distinct()

    # Đếm số lượng file trong mỗi thư mục
    folder_counts = {}
    for folder in folders:
        count = Media.objects.filter(folder_name=folder).count()
        folder_counts[folder] = count

    return JsonResponse({
        'success': True,
        'folders': [{'name': folder, 'count': folder_counts[folder]} for folder in folders]
    })
