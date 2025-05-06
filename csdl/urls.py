from django.urls import path
from csdl import views

urlpatterns = [
    path('add-sample-data/', views.add_sample_data, name='add_sample_data'),
]

