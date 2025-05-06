from django.shortcuts import render
# Create your views here.
def quanlymenu(request):
    return render(request, 'quanlymenu.html')
def get_content(request, target):
    if target == 'quanlybaiviet':
        # Trả về nội dung block bài viết
        context = {
            'baiviet_data': 'Nội dung bài viết mặc định'
        }
        return render(request, 'quanlybaiviet.html', context)
    elif target == 'dashboard':
        context = {
            'dashboard_data': 'Nội dung dashboard'
        }
        return render(request, 'dashboard.html', context)
    elif target == 'quanlythe':
        context = {
            'the_data': 'Nội dung quanlythe'
        }
        return render(request, 'quanlythe.html', context)
    elif target == 'quanlymedia':
        context = {
            'media_data': 'Nội dung quanlymedia'
        }
        return render(request, 'quanlymedia.html', context)
    elif target == 'quanlythanhvien':
        context = {
            'thanhvien_data': 'Nội dung quanlythanhvien'
        }
        return render(request, 'quanlythanhvien.html', context)
    elif target == 'quanlycauhinh':
        context = {
            'cauhinh_data': 'Nội dung quanlycauhinh'
        }
        return render(request, 'quanlycauhinh.html', context)
    elif target == 'quanlymenu':
        context = {
            'quanlymenu_data': 'Nội dung menu'
        }
        return render(request, 'quanlymenu.html', context)

def them_menu(request):
    return render(request, 'themmenu.html')
def xem_menu(request, menu_id):
    # Giả sử bạn sẽ lấy dữ liệu theo category_id từ cơ sở dữ liệu
    context = {
        'menu_id': menu_id,
        'category_data': f'Nội dung menu với ID {menu_id}'  # Bạn có thể thay thế bằng dữ liệu thực tế từ DB
    }
    return render(request, 'xemmenu.html', context)
def sua_menu(request, menu_id):
    # Giả sử bạn sẽ lấy dữ liệu theo category_id từ cơ sở dữ liệu
    context = {
        'menu_id': menu_id,
        'category_data': f'Nội dung menu với ID {menu_id}'  # Bạn có thể thay thế bằng dữ liệu thực tế từ DB
    }
    return render(request, 'suamenu.html', context)