
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    # path('login/', views.tenant_login, name='tenant-login'),
    path('logout/', views.user_logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.create_tenant, name='register'),
    path('dashboard/', views.tenant_dashboard, name='tenant-dashboard'),
    
]
