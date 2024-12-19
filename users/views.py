from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'tenant_profile'):
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


@tenant_required
def tenant_dashboard(request):
    return render(request, 'users/tenant-dashboard.html')


def tenant_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            # Check if user is tenant
            if hasattr(user, 'tenant_profile'):
                login(request, user)
                return redirect('mainweb:index')
            else:
                messages.error(request, "This account is not associated with tenant.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'users/tenant-login.html')

