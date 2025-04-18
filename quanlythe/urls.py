from django.urls import path
from quanlythe import views
urlpatterns = [
    path("",views.quanlythe, name = "quanlythe"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]