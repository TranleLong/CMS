from django.urls import path
from quanlycauhinh import views
urlpatterns = [
    path("",views.quanlycauhinh, name = "qlcauhinh"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]