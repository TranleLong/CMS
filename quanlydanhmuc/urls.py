from django.urls import path
from quanlydanhmuc import views
urlpatterns = [
    path("", views.quanlydanhmuc, name = "quanlydanhmuc"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]