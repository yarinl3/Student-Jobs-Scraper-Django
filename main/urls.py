from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scraped_list/', views.scraped_list, name='scraped_list'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('sent/', views.sent, name='sent'),
    path('scrap/', views.pre_scrap, name='scrap'),
    path('keywords/', views.keywords, name='keywords'),
]
