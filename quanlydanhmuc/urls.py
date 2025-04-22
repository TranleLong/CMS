from django.urls import path
from quanlydanhmuc import views
urlpatterns = [
    path("", views.quanlydanhmuc, name = "quanlydanhmuc"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
    path('get-content/quanlydanhmuc/themdanhmuc/',views.them_danhmuc, name='themdanhmuc'),
    path('get-content/quanlydanhmuc/xemdanhmuc/<int:category_id>/', views.xem_danhmuc, name='xem_danhmuc'),
    path('get-content/quanlydanhmuc/suadanhmuc/<int:category_id>/', views.sua_danhmuc, name='sua_danhmuc'),
]