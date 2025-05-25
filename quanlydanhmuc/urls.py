from django.urls import path
from quanlydanhmuc import views

urlpatterns = [
    path("quanlydanhmuc/", views.quanlydanhmuc, name="quanlydanhmuc"),
    path('quanlydanhmuc/themdanhmuc/', views.them_danhmuc, name='themdanhmuc'),
    path('quanlydanhmuc/xemdanhmuc/<int:category_id>/', views.xem_danhmuc, name='xem_danhmuc'),
    path('quanlydanhmuc/suadanhmuc/<int:category_id>/', views.sua_danhmuc, name='sua_danhmuc'),
    path('quanlydanhmuc/xoa_danhmuc/<int:category_id>/', views.xoa_danhmuc, name='xoa_danhmuc'),
]
