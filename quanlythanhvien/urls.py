from django.urls import path
from quanlythanhvien import views
urlpatterns = [
    path("",views.quanlythanhvien, name = "thanhvien"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]