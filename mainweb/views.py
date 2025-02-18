from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

from accomodations.models import HouseImage, RoomImage, Room, House, Booking
from finances.models import PaymentMethod
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'main-web/index-2.html')

def about(request):
    return render(request, 'main-web/about.html')

def contact(request):
    return render(request, 'main-web/contact-us.html')



def room_list(request):
    """List all rooms and show if they are available for selected dates."""
    
    rooms = Room.objects.all()
    start_date = None
    end_date = None

    if request.method == "POST":
        start_date = request.POST.get("checkIn")
        end_date = request.POST.get("checkOut")

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                if end_date <= start_date:
                    return HttpResponseBadRequest("Check-out date must be after check-in date.")

            except ValueError:
                return HttpResponseBadRequest("Invalid date format. Please use YYYY-MM-DD.")

    # Attach availability info for each room without filtering them out
            for room in rooms:
                room.is_available_for_dates = room.check_availability(start_date, end_date) if start_date and end_date else None

    # Paginate all rooms
    paginator = Paginator(rooms, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, "main-web/room-list.html", context)



def room_details(request, slug, checkin=None, checkout=None):
    room = get_object_or_404(Room, slug=slug)  # Fetch by slug

    if checkin and checkout:
        checkin = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout, "%Y-%m-%d").date()

        if checkout <= checkin:
            return HttpResponseBadRequest("Check-out date must be after check-in date.")

        nights = (checkout - checkin).days  # Fix subtraction
    else:
        checkin = checkout = None
        nights = 1  # Default to 1 night if no dates provided

    property = room.property    

    price_per_night = room.price_per_night
    total_price = price_per_night * nights

    print(f"Slug: {slug}, Check-in: {checkin}, Check-out: {checkout}, Nights: {nights}, Total Price: {total_price}")

    context = {
        'room': room,
        'checkin': checkin.strftime("%Y-%m-%d") if checkin else None,
        'checkout': checkout.strftime("%Y-%m-%d") if checkout else None,
        'total_price': total_price,
        'property': property,        
    }
    return render(request, 'main-web/room.html', context)



def house_list(request):
    """List all houses and show if they are available for selected dates."""
    
    houses = House.objects.all()
    start_date = None
    end_date = None

    if request.method == "POST":
        start_date = request.POST.get("checkIn") or None
        end_date = request.POST.get("checkOut") or None

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                if end_date <= start_date:
                    return HttpResponseBadRequest("Check-out date must be after check-in date.")

    # Attach availability info for each house without filtering
                for house in houses:
                    house.is_available_for_dates = house.check_availability(start_date, end_date) if start_date and end_date else None

            except ValueError:
                return HttpResponseBadRequest("Invalid date format. Please use YYYY-MM-DD.")

    # Paginate only the filtered houses
    paginator = Paginator(houses, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, "main-web/house-list.html", context)




def house_details(request, slug, checkin=None, checkout=None):
    house = get_object_or_404(House, slug=slug)  # Fetch by slug

    if checkin and checkout:
        checkin = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout, "%Y-%m-%d").date()

        if checkout <= checkin:
            return HttpResponseBadRequest("Check-out date must be after check-in date.")

        nights = (checkout - checkin).days  # Fix subtraction
    else:
        checkin = checkout = None
        nights = 1  # Default to 1 night if no dates provided

    property = house.property    

    price_per_night = house.price_per_night
    total_price = price_per_night * nights

    print(f"Slug: {slug}, Check-in: {checkin}, Check-out: {checkout}, Nights: {nights}, Total Price: {total_price}")

    context = {
        'house': house,
        'checkin': checkin.strftime("%Y-%m-%d") if checkin else None,
        'checkout': checkout.strftime("%Y-%m-%d") if checkout else None,
        'total_price': total_price,
        'property': property,        
    }
    print(house.id)
    return render(request, 'main-web/house-details.html', context)


def payment_methods(request, type, id):
    # Determine whether it's a House or a Room
    if type == "house":
        obj = get_object_or_404(House, id=id)
        image = HouseImage.objects.filter(house=obj).first()
    elif type == "room":
        obj = get_object_or_404(Room, id=id)
        image = RoomImage.objects.filter(room=obj).first()
    else:
        return render(request, '404.html')  # Handle invalid type

    payment_methods = PaymentMethod.objects.all()

    # Get dates from request
    checkin = request.GET.get('checkIn')
    checkout = request.GET.get('checkOut')

    # Default values if no dates are provided
    if checkin and checkout:
        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        total_nights = (checkout_date - checkin_date).days
    else:
        checkin_date = None
        checkout_date = None
        total_nights = 1  # Default to 1 night

    # Calculate price
    total_price = obj.price_per_night * total_nights

    return render(request, 'main-web/payment-methods.html', {
        'obj': obj,
        'image': image,
        'payment_methods': payment_methods,
        'checkin_date': checkin_date.strftime("%Y-%m-%d"),
        'checkout_date': checkout_date.strftime("%Y-%m-%d"),
        'total_nights': total_nights,
        'total_price': total_price,
        'type': type,  # Pass the type to the template
    })




def confirm_booking(request, type, id):
    print("DEBUG: confirm_booking function called")  # Debug print

    if request.method != "POST":
        print("DEBUG: Invalid request method")
        messages.error(request, "Invalid request.")
        return redirect('mainweb:index')

    if not request.user.is_authenticated:
        print("DEBUG: User not authenticated")
        messages.error(request, "Please log in to confirm your booking.")
        return redirect('users:login')

    checkin = request.POST.get('checkIn')
    checkout = request.POST.get('checkOut')
    print(f"DEBUG: Received check-in: {checkin}, check-out: {checkout}")  # Debug print

    if not checkin or not checkout:
        print("DEBUG: Missing booking dates")
        messages.error(request, "Missing booking dates.")
        return redirect('mainweb:payment-methods', type=type, id=id)

    try:
        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        print(f"DEBUG: Parsed dates - Check-in: {checkin_date}, Check-out: {checkout_date}")  # Debug print
    except ValueError:
        print("DEBUG: Invalid date format")
        messages.error(request, "Invalid date format.")
        return redirect('mainweb:payment-methods', type=type, id=id)

    if checkout_date <= checkin_date:
        print("DEBUG: Invalid check-in/check-out logic")
        messages.error(request, "Check-out must be after check-in.")
        return redirect('mainweb:payment-methods', type=type, id=id)

    # Get the house or room object
    if type == 'house':
        obj = get_object_or_404(House, id=id)
        print(f"DEBUG: House selected - {obj.name}")  # Debug print
        booking = Booking.objects.create(
            tenant=request.user,  # Correctly linking the tenant to the User model
            house=obj,
            check_in=checkin_date,
            check_out=checkout_date,
            status="pending"  # Set status to pending
        )
    elif type == 'room':
        obj = get_object_or_404(Room, id=id)
        print(f"DEBUG: Room selected - {obj.name}")  # Debug print
        booking = Booking.objects.create(
            tenant=request.user,  # Correctly linking the tenant to the User model
            room=obj,
            check_in=checkin_date,
            check_out=checkout_date,
            status="pending"  # Set status to pending
        )
    else:
        print("DEBUG: Invalid booking type")
        messages.error(request, "Invalid booking type.")
        return redirect('mainweb:index')

    # Email Settings (Use your email address)
    from_email = "rizwansoomro@gmail.com"  # Replace with your email
    recipient_list = ['rizwansoomro@gmail.com']  # Send email to this address
    subject = "New Booking Request"
    message = (
        f"A new booking request has been made:\n\n"
        f"Tenant: {request.user.username} ({request.user.email})\n"
        f"Property: {obj.name}\n"
        f"Check-in: {checkin_date}\n"
        f"Check-out: {checkout_date}\n"
        f"Status: Pending\n\n"
        "Please review and confirm the booking."
    )

    try:
        print("DEBUG: Sending email...")
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("DEBUG: Email sent successfully")
        messages.success(request, "Booking request submitted. You will be contacted soon.")
    except Exception as e:
        print(f"DEBUG: Email failed to send - {e}")
        messages.error(request, f"Booking was created, but email failed: {e}")

    print("DEBUG: Redirecting to tenant dashboard")
    return redirect('users:tenant-dashboard')  # Redirect user to tenant dashboard




