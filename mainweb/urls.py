
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'mainweb'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('room-list/', views.room_list, name='room-list'),
    path('room/<slug:slug>/', views.room_details, name='room-details'),
    path('house-list/', views.house_list, name='house-list'),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
