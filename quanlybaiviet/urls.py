from django.urls import path
from . import views

urlpatterns = [
    path('quanlybaiviet/', views.quanlybaiviet, name='quanlybaiviet'),
    path('quanlybaiviet/thembaiviet/', views.them_baiviet, name='them_baiviet'),
    path('quanlybaiviet/xembaiviet/<int:bai_viet_id>/', views.xem_baiviet, name='xem_baiviet'),
    path('quanlybaiviet/suabaiviet/<int:bai_viet_id>/', views.sua_baiviet, name='sua_baiviet'),
    path('quanlybaiviet/xoabaiviet/<int:bai_viet_id>/', views.xoa_baiviet, name='xoa_baiviet'),
    # Thêm API để lấy danh sách media
    path('api/media/', views.api_media_list, name='api_media_list'),
    # Thêm API để lấy URL của một media cụ thể
    path('api/media/<int:media_id>/', views.get_media_url, name='get_media_url'),
]