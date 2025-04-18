from django.urls import path
from quanlymenu import views
urlpatterns = [
    path("",views.quanlymenu, name = "quanlymenu"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]