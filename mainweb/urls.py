
from django.urls import path, include

from . import views

app_name = 'mainweb'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
]
