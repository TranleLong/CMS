from django.urls import path
from . import views

urlpatterns = [
    path('quanlythe/', views.quanlythe, name='quanlythe'),
    path('quanlythe/themthe/', views.them_the, name='them_the'),
    path('quanlythe/xemthe/<int:tag_id>/', views.xem_the, name='xem_the'),
    path('quanlythe/suathe/<int:tag_id>/', views.sua_the, name='sua_the'),
    path('quanlythe/xoathe/<int:tag_id>/', views.xoa_the, name='xoa_the'),
]
