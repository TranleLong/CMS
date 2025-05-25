from django.urls import path
from . import views

urlpatterns = [
    path('quanlymedia/', views.quanlymedia, name='quanlymedia'),
    path('quanlymedia/upload/', views.upload_media, name='upload_media'),
    path('quanlymedia/create-folder/', views.create_folder, name='create_folder'),
    path('quanlymedia/view/<int:media_id>/', views.view_media, name='view_media'),
    path('quanlymedia/download/<int:media_id>/', views.download_media, name='download_media'),
    path('quanlymedia/download-folder/<str:folder_name>/', views.download_folder, name='download_folder'),
    path('quanlymedia/delete/<int:media_id>/', views.delete_media, name='delete_media'),
    path('quanlymedia/delete-folder/<str:folder_name>/', views.delete_folder, name='delete_folder'),
    path('quanlymedia/get-folders/', views.get_folders, name='get_folders'),
]
