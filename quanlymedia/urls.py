from django.urls import path
from quanlymedia import views
urlpatterns = [
    path("",views.quanlymedia, name = "quanlymedia"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]