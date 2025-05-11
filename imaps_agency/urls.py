from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('mission/', views.mission, name='mission'),
    path('contact/', views.contact, name='contact'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    re_path(r'^imaps/articles/(?P<url>.+)/$', views.article_detail, name='article_detail'),
]