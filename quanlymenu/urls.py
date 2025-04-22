from django.urls import path
from quanlymenu import views
urlpatterns = [
    path("",views.quanlymenu, name = "quanlymenu"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
    path('get-content/quanlymenu/themmenu/',views.them_menu, name='themmenu'),
    path('get-content/quanlymenu/xemmenu/<int:menu_id>/', views.xem_menu, name='xem_menu'),
    path('get-content/quanlymenu/suamenu/<int:menu_id>/', views.sua_menu, name='sua_menu'),
]