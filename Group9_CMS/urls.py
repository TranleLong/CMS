"""
URL configuration for Group9_CMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import quanlythe include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from Group9_CMS import settings
from dashboard import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard, name = 'dashboard'),
    path('', include('csdl.urls')),
    path('', include('dashboard.urls')),
    path('', include('quanlybaiviet.urls')),
    path('', include('quanlydanhmuc.urls')),
    path('', include('quanlycauhinh.urls')),
    path('', include('quanlythe.urls')),
    path('', include('quanlymedia.urls')),
    path('', include('quanlythanhvien.urls')),
    path('', include('quanlymenu.urls')),
    path('', include('imaps.urls')),  # Thêm URL của app imaps

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)