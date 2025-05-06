# from django.urls import path
# from quanlybaiviet import views
# urlpatterns = [
#     path("", views.qlbaiviet, name = "quanlybaiviet"),
#     path('get-content/<str:target>/', views.get_content, name='get_content'),
#     path('get-content/<str:target>/suabaiviet/', views.sua_baiviet, name='suabaiviet'),
#     path('get-content/<str:target>/thembaiviet/', views.them_baiviet, name='thembaiviet'),
#     path('get-content/<str:target>/xembaiviet/', views.xem_baiviet, name='xembaiviet'),
#
# ]
#
# from django.urls import path
# from quanlybaiviet import views
# urlpatterns = [
#     path("quanlybaiviet/", views.qlbaiviet, name = "quanlybaiviet"),
#     path('<str:target>/suabaiviet/', views.sua_baiviet, name='suabaiviet'),
#     path('get-content/<str:target>/thembaiviet/', views.them_baiviet, name='thembaiviet'),
#     path('<str:target>/xembaiviet/', views.xem_baiviet, name='xembaiviet'),
# ]


# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('quanlybaiviet/', views.quanlybaiviet, name='quanlybaiviet'),
#     path('quanlybaiviet/thembaiviet/', views.them_baiviet, name='them_baiviet'),
#     path('quanlybaiviet/xembaiviet/<int:bai_viet_id>/', views.xem_baiviet, name='xem_baiviet'),
#     path('quanlybaiviet/suabaiviet/<int:bai_viet_id>/', views.sua_baiviet, name='sua_baiviet'),
#     path('quanlybaiviet/xoabaiviet/<int:bai_viet_id>/', views.xoa_baiviet, name='xoa_baiviet'),
#     path('get-content/<str:target>/', views.get_content, name='get_content'),
# ]
#
from django.urls import path
from . import views

urlpatterns = [
    path('quanlybaiviet/', views.quanlybaiviet, name='quanlybaiviet'),
    path('quanlybaiviet/thembaiviet/', views.them_baiviet, name='them_baiviet'),
    path('quanlybaiviet/xembaiviet/<int:bai_viet_id>/', views.xem_baiviet, name='xem_baiviet'),
    path('quanlybaiviet/suabaiviet/<int:bai_viet_id>/', views.sua_baiviet, name='sua_baiviet'),
    path('quanlybaiviet/xoabaiviet/<int:bai_viet_id>/', views.xoa_baiviet, name='xoa_baiviet'),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]
