from django.urls import path
from quanlythanhvien import views
urlpatterns = [
    path("",views.quanlythanhvien, name = "thanhvien"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
    path('get-content/quanlythanhvien/themthanhvien/',views.them_thanhvien, name='them_thanhvien'),
    path('get-content/quanlythanhvien/xemthanhvien/<int:member_id>/', views.xem_thanhvien, name='xem_thanhvien'),
    path('get-content/quanlythanhvien/suathanhvien/<int:member_id>/', views.sua_thanhvien, name='sua_thanhvien'),
]