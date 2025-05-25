from django.urls import path
from quanlycauhinh import views

urlpatterns = [
    path("quanlycauhinh/", views.quanlycauhinh, name="quanlycauhinh"),

    # Đường dẫn cho quản lý liên hệ
    path('quanlycauhinh/contact/', views.contact_list, name='contact_list'),
    path('quanlycauhinh/contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('quanlycauhinh/contact/<int:contact_id>/note/', views.contact_note, name='contact_note'),
    path('quanlycauhinh/contact/<int:contact_id>/delete/', views.contact_delete, name='contact_delete'),
]