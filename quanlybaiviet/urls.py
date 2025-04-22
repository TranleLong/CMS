from django.urls import path
from quanlybaiviet import views
urlpatterns = [
    path("", views.qlbaiviet, name = "quanlybaiviet"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
    path('get-content/<str:target>/suabaiviet/', views.sua_baiviet, name='suabaiviet'),
    path('get-content/<str:target>/thembaiviet/', views.them_baiviet, name='thembaiviet'),
    path('get-content/<str:target>/xembaiviet/', views.xem_baiviet, name='xembaiviet'),
]