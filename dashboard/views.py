from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from csdl.models import BaiViet, DanhMuc, Media
from django.contrib.auth.models import User
from datetime import timedelta

@login_required(login_url='login')
def dashboard(request):
    # 1. Lấy tham số từ request từ ng dùng
    filters = get_filter_params(request)
    # 2. Lấy dữ liệu thống kê
    stats = get_statistics(filters)
    # 3. Lấy dữ liệu biểu đồ
    chart_data = get_chart_data(filters['chart_year'])
    # 4. Lấy hoạt động gần đây
    activities = get_recent_activities()
    # 5. Chuẩn bị context để render template
    context = {
        # Thống kê
        'total_bai_viet': stats['total_bai_viet'],
        'bai_viet_trong_thang': stats['bai_viet_trong_thang'],
        'total_danh_muc': stats['total_danh_muc'],
        'danh_muc_trong_thang': stats['danh_muc_trong_thang'],
        'total_media': stats['total_media'],
        'media_trong_thang': stats['media_trong_thang'],
        'total_thanh_vien': stats['total_thanh_vien'],
        'thanh_vien_trong_thang': stats['thanh_vien_trong_thang'],

        # Biểu đồ
        'chart_data': chart_data['data'],
        'max_chart_value': chart_data['max_value'],
        'y_values': chart_data['y_values'],

        # Hoạt động gần đây
        'recent_activities': activities,

        # Tham số lọc
        'selected_day': filters['day'],
        'selected_month': filters['month'],
        'selected_year': filters['year'],
        'chart_year': filters['chart_year'],

        # Danh sách cho dropdown
        'days': list(range(1, 32)),
        'months': get_month_list(),
        'years': list(range(timezone.now().year - 5, timezone.now().year + 1)),

        # Tiêu đề
        'filter_title': filters['filter_title'],
    }
    return render(request, 'dashboard.html', context)

# lấy tất cả tham số
def get_filter_params(request):
    # Lấy tham số từ request
    day = request.GET.get('day', '')
    # '' là nếu ko có giá trị thì thay cho day: ko có giá trị cx đc
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    chart_year = request.GET.get('chart_year', timezone.now().year)
    # Xử lý tham số ngày
    try:
        day = int(day) if day and 1 <= int(day) <= 31 else ''
    except (ValueError, TypeError):
        day = ''
    # Xử lý tham số tháng
    try:
        month = int(month) if month and 1 <= int(month) <= 12 else ''
    except (ValueError, TypeError):
        month = ''

    # Xử lý tham số năm
    current_year = timezone.now().year
    try:
        year = int(year) if year and current_year - 10 <= int(year) <= current_year + 1 else ''
    except (ValueError, TypeError):
        year = ''

    # Xử lý tham số năm cho biểu đồ
    try:
        chart_year = int(chart_year) if current_year - 10 <= int(chart_year) <= current_year + 1 else current_year
    except (ValueError, TypeError):
        chart_year = current_year

    # Tạo tiêu đề cho bộ lọc
    filter_title = create_filter_title(day, month, year)

    return {
        'day': day,
        'month': month,
        'year': year,
        'chart_year': chart_year,
        'filter_title': filter_title
    }


def create_filter_title(day, month, year):
    """Tạo tiêu đề dựa trên bộ lọc đã chọn"""
    if day and month and year:
        return f"Ngày {day}/{month}/{year}"
    elif month and year:
        month_name = get_month_name(month)
        return f"{month_name} năm {year}"
    elif year:
        return f"Năm {year}"
    else:
        return "Tất cả dữ liệu"


def get_month_name(month_number):
    """Lấy tên tháng từ số tháng"""
    months = get_month_list()
    for month in months:
        if month['value'] == month_number:
            return month['name']
    return f"T{month_number}"


def get_month_list():
    return [
        {'value': 1, 'name': 'Tháng 1'},
        {'value': 2, 'name': 'Tháng 2'},
        {'value': 3, 'name': 'Tháng 3'},
        {'value': 4, 'name': 'Tháng 4'},
        {'value': 5, 'name': 'Tháng 5'},
        {'value': 6, 'name': 'Tháng 6'},
        {'value': 7, 'name': 'Tháng 7'},
        {'value': 8, 'name': 'Tháng 8'},
        {'value': 9, 'name': 'Tháng 9'},
        {'value': 10, 'name': 'Tháng 10'},
        {'value': 11, 'name': 'Tháng 11'},
        {'value': 12, 'name': 'Tháng 12'},
    ]


def get_statistics(filters):
    """Lấy dữ liệu thống kê dựa trên bộ lọc"""
    # Xây dựng bộ lọc cho thống kê
    filter_query = build_date_filter(filters['day'], filters['month'], filters['year'])

    # Lấy thời điểm đầu tháng hiện tại
    first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Nếu có bộ lọc
    if filter_query:
        # Lấy số bài viết theo bộ lọc
        total_bai_viet = BaiViet.objects.filter(**filter_query).count()

        # Lấy số bài viết mới trong tháng (trong phạm vi bộ lọc)
        bai_viet_trong_thang_filter = {**filter_query, 'ngay_dang__gte': first_day_of_month}
        bai_viet_trong_thang = BaiViet.objects.filter(**bai_viet_trong_thang_filter).count()

        # Lấy số thành viên theo bộ lọc
        user_filter = convert_filter_for_users(filter_query)
        if user_filter:
            total_thanh_vien = User.objects.filter(**user_filter).count()
            thanh_vien_trong_thang_filter = {**user_filter, 'date_joined__gte': first_day_of_month}
            thanh_vien_trong_thang = User.objects.filter(**thanh_vien_trong_thang_filter).count()
        else:
            total_thanh_vien = User.objects.count()
            thanh_vien_trong_thang = User.objects.filter(date_joined__gte=first_day_of_month).count()
    else:
        # Không có bộ lọc, hiển thị tất cả dữ liệu
        total_bai_viet = BaiViet.objects.count()
        bai_viet_trong_thang = BaiViet.objects.filter(ngay_dang__gte=first_day_of_month).count()
        total_thanh_vien = User.objects.count()
        thanh_vien_trong_thang = User.objects.filter(date_joined__gte=first_day_of_month).count()

    # Lấy số danh mục và media (không phụ thuộc vào bộ lọc thời gian)
    total_danh_muc = DanhMuc.objects.count()
    danh_muc_trong_thang = DanhMuc.objects.filter(order_index__gt=0).count()
    total_media = Media.objects.count()
    media_trong_thang = Media.objects.filter(ma_media__gt=0).count()

    return {
        'total_bai_viet': total_bai_viet,
        'bai_viet_trong_thang': bai_viet_trong_thang,
        'total_danh_muc': total_danh_muc,
        'danh_muc_trong_thang': danh_muc_trong_thang,
        'total_media': total_media,
        'media_trong_thang': media_trong_thang,
        'total_thanh_vien': total_thanh_vien,
        'thanh_vien_trong_thang': thanh_vien_trong_thang,
    }

# hàm này bộ lọc trên ngày tháng năm
def build_date_filter(day, month, year):
    """Xây dựng bộ lọc dựa trên ngày, tháng, năm"""
    if not any([day, month, year]):
        return {}

    filter_query = {}
    # Xử lý khi có đầy đủ ngày, tháng, năm
    if day and month and year:
        start_date = timezone.datetime(year, month, day).date()
        end_date = start_date
    # Chỉ có tháng + năm
    elif month and year:
        start_date = timezone.datetime(year, month,1)
        last_day = monthrange(year, month)[1]
        end_date = timezone.datetime(year, month, last_day)
    # Chỉ có ngày và năm
    elif day and year:
        start_date = timezone.datetime(year, 1, day)
        end_date = timezone.datetime(year, 12, day)
    else:
        return {}

    filter_query['ngay_dang__gte'] = start_date
    filter_query['ngay_dang__lte'] = end_date

    return filter_query

# Kiểm tra số ngày trong tháng
def get_days_in_month(month, year):
    if month == 2:
        return 29 if ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31



def convert_filter_for_users(filter_query):
    """Chuyển đổi bộ lọc từ ngay_dang sang date_joined cho User"""
    if not filter_query:
        return {}

    user_filter = {}
    if 'ngay_dang__gte' in filter_query:
        user_filter['date_joined__gte'] = filter_query['ngay_dang__gte']
    if 'ngay_dang__lte' in filter_query:
        user_filter['date_joined__lte'] = filter_query['ngay_dang__lte']

    return user_filter


def get_chart_data(year):
    """Lấy dữ liệu cho biểu đồ theo năm"""
    chart_data = [] # chứa dữ liệu chi tiết cho từng tháng, gồm tháng, số bài viết, chiều cao cột biểu đồ.
    monthly_counts = [] #  chứa số lượng bài viết của từng tháng (chỉ số nguyên).

    # Lấy số bài viết theo từng tháng trong năm
    for month in range(1, 13):
        start_date = timezone.datetime(year, month, 1)
        if month == 12:
            end_date = timezone.datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = timezone.datetime(year, month + 1, 1) - timedelta(seconds=1)

        count = BaiViet.objects.filter(ngay_dang__gte=start_date, ngay_dang__lte=end_date).count()
        monthly_counts.append(count) # chứa số lượng bài viết của từng tháng

        # Tính chiều cao cho biểu đồ
        max_count_for_scale = max(monthly_counts) if max(monthly_counts) > 0 else 1
        height_percentage = (count / max_count_for_scale) * 100
        height = height_percentage

        chart_data.append({
            'month': f"T{month}",
            'count': count,
            'height': height
        })

    # Tìm giá trị lớn nhất để hiển thị trên trục Y
    max_count = max(monthly_counts) if monthly_counts else 0

    # Tính toán các giá trị cho trục Y
    y_values = [
        max_count,
        int(max_count * 0.75),
        int(max_count * 0.5),
        int(max_count * 0.25),
        0
    ]

    return {
        'data': chart_data, #  danh sách dữ liệu biểu đồ theo tháng.
        'max_value': max_count, # giá trị lớn nhất trong năm.
        'y_values': y_values # danh sách nhãn trục Y.
    }


def get_recent_activities():
    activities = []

    # Lấy bài viết mới nhất
    recent_posts = BaiViet.objects.select_related('ma_nguoi_dung').order_by('-ngay_dang')[:5]
    for post in recent_posts:
        activities.append({
            'type': 'post',
            'user': post.ma_nguoi_dung.last_name,
            'action': f'đã tạo bài viết {post.tieu_de}',
            'time': post.ngay_dang,
            'icon': 'fas fa-file-alt'
        })

    # Sắp xếp theo thời gian
    activities = sorted(activities, key=lambda x: x['time'], reverse=True)[:10]

    # Định dạng thời gian hiển thị
    for activity in activities:
        format_activity_time(activity)

    return activities

def format_activity_time(activity):
    """Định dạng thời gian hiển thị cho hoạt động"""
    now = timezone.now()
    time_diff = now.date() - activity['time'].date() if hasattr(activity['time'], 'date') else now.date() - activity[
        'time']

    if time_diff.days == 0:
        # Kiểm tra xem activity['time'] có thuộc tính hour không
        if hasattr(activity['time'], 'hour'):
            hours_diff = now.hour - activity['time'].hour
            if hours_diff <= 0:
                activity['time_display'] = 'Vừa xong'
            else:
                activity['time_display'] = f'{hours_diff} giờ trước'
        else:
            # Nếu không có thuộc tính hour, giả định là 'Hôm nay'
            activity['time_display'] = 'Hôm nay'
    elif time_diff.days == 1:
        activity['time_display'] = 'Hôm qua'
    else:
        activity['time_display'] = f'{time_diff.days} ngày trước'

    return activity