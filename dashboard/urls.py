from django.urls import path
from dashboard import views
urlpatterns = [
    path("", views.dashboard, name = "dashboard"),
    path('get-content/<str:target>/', views.get_content, name='get_content'),
]