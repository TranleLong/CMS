from django.urls import path
from quanlybaiviet import views
urlpatterns = [
    path("", views.qlbaiviet, name = "quanlybaiviet"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
    path('get-content/<str:target>/suabaiviet/', views.sua_baiviet, name='suabaiviet'),
    path('suabaiviet/', views.sua_baiviet, name='sua_baiviet'),
    path('get-content/<str:target>/thembaiviet/', views.them_baiviet, name='thembaiviet'),
    path('thembaiviet/', views.them_baiviet, name='them_baiviet'),
    path('get-content/<str:target>/xembaiviet/', views.xem_baiviet, name='xembaiviet'),
    path('xembaiviet/', views.xem_baiviet, name='xem_baiviet'),
]