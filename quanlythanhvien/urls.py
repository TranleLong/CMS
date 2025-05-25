from django.urls import path
from . import views

urlpatterns = [
    path('quanlythanhvien/', views.quanlythanhvien, name='quanlythanhvien'),
    path('quanlythanhvien/themthanhvien/', views.them_thanh_vien, name='them_thanh_vien'),
    path('quanlythanhvien/xemthanhvien/<int:user_id>/', views.xem_thanh_vien, name='xem_thanh_vien'),
    path('quanlythanhvien/suathanhvien/<int:user_id>/', views.sua_thanh_vien, name='sua_thanh_vien'),
    path('quanlythanhvien/xoathanhvien/<int:user_id>/', views.xoa_thanh_vien, name='xoa_thanh_vien'),
]
