from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Sử dụng authenticate để khi mà đúng là trả về user
        # Còn sai là trả về none
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # dòng này để lưu cái phiên đăng nhập của người đó lại để bk ng đó là ai
            auth_login(request, user)
            # nếu ko có thì mặc dù đã nhập đúng tk mật khẩu thì coi như cx chưa đăng nhập
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error_message': 'Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.'
            })
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    # Xóa phiên đăng nhập
    return redirect('login')

# phân quyền cho người dùng
# {% if not request.user.groups.all.0.id == 2 %}:
# {% endif %}
# lấy ra tất cả group id của ng dung ở đây là group(1,2)
# rồi lấy phẩn tử đầu tiên so sánh vì người có thứ tự đầu tiên thường là người toàn quyền
# Nếu mà group id đó bằng 2 thì là nhân viên và 1 là quản lý