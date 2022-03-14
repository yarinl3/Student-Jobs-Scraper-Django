from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job_list/', views.job_list, name='job_list'),
    path('scrap/', views.scrap, name='scrap'),
]
