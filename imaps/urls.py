from django.urls import path
from . import views

urlpatterns = [
    path('imaps/', views.home, name='home'),
    path('lien-he/', views.contact, name='contact'),
    path('dich-vu/<slug:slug>/', views.service_detail, name='service_detail'),
    path('bai-viet/<slug:slug>/', views.article_detail, name='article_detail'),

]