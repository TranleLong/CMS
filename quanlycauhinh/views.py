from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from csdl.models import Contact
import json
from django.db.models import Q, Count, Case, When, IntegerField
@login_required(login_url='login')
def quanlycauhinh(request):
    return render(request, "quanlycauhinh.html")


def contact_list(request):
    # Xử lý tìm kiếm và lọc
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')

    contacts = Contact.objects.all()
    # Tính toán thống kê
    stats = Contact.objects.aggregate(
        total_count=Count('ma_lien_he'),
        processed_count=Count(
            Case(
                When(trang_thai='da_xu_ly', then=1),
                output_field=IntegerField()
            )
        ),
        new_count=Count(
            Case(
                When(trang_thai='moi', then=1),
                output_field=IntegerField()
            )
        )
    )

    # Và trong context thêm:

    # Tìm kiếm
    if search_query:
        contacts = contacts.filter(
            Q(ho_ten__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(so_dien_thoai__icontains=search_query) |
            Q(chu_de__icontains=search_query)
        )

    # Lọc theo trạng thái
    if status_filter == 'new':
        contacts = contacts.filter(trang_thai='moi')
    elif status_filter == 'processed':
        contacts = contacts.filter(trang_thai='da_xu_ly')

    # Phân trang
    paginator = Paginator(contacts, 10)  # 10 liên hệ mỗi trang
    page_number = request.GET.get('page', 1)
    contacts_page = paginator.get_page(page_number)

    context = {
        'contacts': contacts_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': stats['total_count'],
        'processed_count': stats['processed_count'],
        'new_count': stats['new_count'],
    }
    return render(request, 'quanlycontact.html', context)


# Xem chi tiết liên hệ
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, ma_lien_he=contact_id)

    data = {
        'ma_lien_he': contact.ma_lien_he,
        'ho_ten': contact.ho_ten,
        'email': contact.email,
        'so_dien_thoai': contact.so_dien_thoai,
        'chu_de': contact.chu_de,
        'noi_dung': contact.noi_dung,
        'ngay_gui': contact.ngay_gui.isoformat(),
        'ghi_chu': contact.ghi_chu,
        'trang_thai': contact.trang_thai
    }

    return JsonResponse(data)


# Lưu ghi chú và trạng thái cho liên hệ
def contact_note(request, contact_id):
    if request.method == 'POST':
        try:
            contact = get_object_or_404(Contact, ma_lien_he=contact_id)
            data = json.loads(request.body)
            contact.ghi_chu = data.get('ghi_chu', '')
            contact.trang_thai = data.get('trang_thai', 'moi')
            contact.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Xóa liên hệ
def contact_delete(request, contact_id):
    if request.method == 'POST':
        try:
            contact = get_object_or_404(Contact, ma_lien_he=contact_id)
            contact.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})