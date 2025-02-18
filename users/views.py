from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TenantRegistrationForm
from .models import TenantProfile
from django.contrib.auth.models import User
from finances.models import Payment
from accomodations.models import Booking, Property, Room
# Create your views here.


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'tenant_profile'):
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def tenant_dashboard(request):
    try:
        tenant_profile = request.user.tenant_profile
    except TenantProfile.DoesNotExist:
        messages.error(request, "Tenant profile not found. Please complete your profile.")
        return redirect('users:create-profile')
    
    # Get the latest active booking for the tenant
    booking = Booking.objects.filter(tenant=request.user).order_by('-created_at').first()

    # Debugging step
    print(f"Booking: {booking}")

    # Get property managers if a booking exists
    managers = []
    if booking:
        property_obj = booking.house.property if booking.house else booking.room.property if booking.room else None
        print(f"Property: {property_obj}")  # Debugging: Check if property exists

        if property_obj:
            managers = property_obj.assigned_managers.all()
            print(f"Managers: {list(managers)}")  # Debugging: Check managers
    
    # Get payments for the tenant
    payments = Payment.objects.filter(booking__tenant=request.user).order_by('-created_at')

    context = {
        'tenant_profile': tenant_profile,
        'booking': booking,
        'managers': managers,
        'payments': payments,
    }

    return render(request, 'users/tenant-dashboard.html', context)






def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('mainweb:index')  # Redirect to your homepage or login page



def tenant_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            # Check if user is tenant
            if hasattr(user, 'tenant_profile'):
                login(request, user)
                
                # Get 'next' parameter from the query string, if it exists
                next_url = request.GET.get('next', 'mainweb:index')

                # If the 'next' URL is for payment-methods, append the query parameters for checkin and checkout
                if 'payment-methods' in next_url:
                    checkin_date = request.GET.get('checkIn', '')
                    checkout_date = request.GET.get('checkOut', '')
                    next_url = f"{next_url}?checkIn={checkin_date}&checkOut={checkout_date}"

                return HttpResponseRedirect(next_url)  # Redirect back to the payment methods page or the default page
            else:
                messages.error(request, "This account is not associated with tenant.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'users/tenant-login.html')


def create_tenant(request):
    if request.method == 'POST':
        form = TenantRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']

            print(username, email)

            try:
                # Check if username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already taken")
                    return render(request, 'users/registration.html', {'form': form})
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already registered")
                    return render(request, 'users/registration.html', {'form': form})

                # Create User
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create Tenant Profile
                TenantProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    address=address
                )

                # Auto-login and redirect
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('mainweb:index')  # Change 'mainweb:index' to your home page

            except Exception as e:
                # Log the error (optional)
                print(f"Error during tenant creation: {e}")
                # Display a generic error message to the user
                messages.error(request, "An error occurred during registration. Please try again.")
                return render(request, 'users/registration.html', {'form': form})

    else:
        form = TenantRegistrationForm()

    return render(request, 'users/registration.html', {'form': form})