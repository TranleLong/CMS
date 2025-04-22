from django.urls import path
from quanlythe import views
urlpatterns = [
    path("",views.quanlythe, name = "quanlythe"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
    path('get-content/quanlythe/themthe/', views.them_the, name='them_the'),
    path('get-content/quanlythe/xemthe/<int:tag_id>/', views.xem_the, name='xem_the'),
    path('get-content/quanlythe/suathe/<int:tag_id>/', views.sua_the, name='sua_the'),
]