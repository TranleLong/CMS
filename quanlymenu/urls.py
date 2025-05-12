from django.urls import path
from . import views

urlpatterns = [
    path("quanlymenu/", views.quanlymenu, name="quanlymenu"),
    path('quanlymenu/themmenu/', views.them_menu, name='themmenu'),
    path('quanlymenu/xemmenu/<int:menu_id>/', views.xem_menu, name='xem_menu'),
    path('quanlymenu/suamenu/<int:menu_id>/', views.sua_menu, name='sua_menu'),
    path('quanlymenu/xoamenu/<int:menu_id>/', views.xoa_menu, name='xoa_menu'),
    path('quanlymenu/xemtruocmenu/<int:menu_id>/', views.xem_truoc_menu, name='xemtruocmenu'),
]
