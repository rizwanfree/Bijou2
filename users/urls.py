
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', views.tenant_login, name='tenant-login'),
    path('logout/', LogoutView.as_view(next_page='mainweb:index', redirect_field_name=None), name='tenant-logout'),
    path('dashboard/', views.tenant_dashboard, name='tenant-dashboard'),
    
]
