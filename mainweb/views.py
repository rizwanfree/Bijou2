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
    amenities = property.amenities.all()  # Retrieve all amenities for the property

    price_per_night = room.price_per_night
    total_price = price_per_night * nights

    print(f"Slug: {slug}, Check-in: {checkin}, Check-out: {checkout}, Nights: {nights}, Total Price: {total_price}")
    print(amenities)
    context = {
        'room': room,
        'checkin': checkin.strftime("%Y-%m-%d") if checkin else None,
        'checkout': checkout.strftime("%Y-%m-%d") if checkout else None,
        'total_price': total_price,
        'property': property,
        'amenities': amenities        
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
    amenities = property.amenities.all()  # Retrieve all amenities for the property
    price_per_night = house.price_per_night
    total_price = price_per_night * nights

    # print(f"Slug: {slug}, Check-in: {checkin}, Check-out: {checkout}, Nights: {nights}, Total Price: {total_price}")

    context = {
        'house': house,
        'checkin': checkin.strftime("%Y-%m-%d") if checkin else None,
        'checkout': checkout.strftime("%Y-%m-%d") if checkout else None,
        'total_price': total_price,
        'property': property,
        'amenities': amenities         
    }
    
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

    # Email Settings
    from_email = "rizwansoomro@gmail.com"  # Replace with your email
    admin_recipient = ['rizwansoomro@gmail.com','skhan.bijou@gmail.com']  # Admin email
    tenant_recipient = [request.user.email]  # Authenticated user's email

    # Get Tenant Details
    first_name = request.user.first_name
    last_name = request.user.last_name
    phone_number = request.user.tenant_profile.phone_number  # Assuming phone number is in the profile model

    # Email Subject
    subject_admin = "New Booking Request"
    subject_tenant = "Booking Confirmation - Pending Payment"

    # Message to Admin
    message_admin = (
        f"A new booking request has been made:\n\n"
        f"👤 Tenant: {first_name} {last_name}\n"
        f"📧 Email: {request.user.email}\n"
        f"📞 Phone: {phone_number}\n"
        f"🏠 Property: {obj.name}\n"
        f"📅 Check-in Date: {checkin_date}\n"
        f"📅 Check-out Date: {checkout_date}\n"
        f"🛑 Status: Pending\n\n"
        "Please review and confirm the booking."
    )

    # Message to Tenant
    message_tenant = (
        f"Dear {first_name} {last_name},\n\n"
        f"Thank you for your booking request! Your booking details are as follows:\n\n"
        f"🏠 Property: {obj.name}\n"
        f"📅 Check-in Date: {checkin_date}\n"
        f"📅 Check-out Date: {checkout_date}\n"
        f"🛑 Status: Pending (Payment Required)\n\n"
        "📞 Contact Support: +123456789 (for any inquiries)\n\n"
        "Your booking is currently in a pending state. We will confirm it once we receive the payment.\n"
        "If you have any questions, feel free to contact us.\n\n"
        "Best Regards,\nBijou Team"
    )

    try:
        # Send email to admin
        print("DEBUG: Sending email to admin...")
        send_mail(subject_admin, message_admin, from_email, admin_recipient, fail_silently=False)
        print("DEBUG: Email to admin sent successfully")

        # Send email to tenant
        print("DEBUG: Sending email to tenant...")
        send_mail(subject_tenant, message_tenant, from_email, tenant_recipient, fail_silently=False)
        print("DEBUG: Email to tenant sent successfully")

        messages.success(request, "Booking request submitted. A confirmation email has been sent.")

        return redirect('users:tenant-dashboard')
    except Exception as e:
        print(f"DEBUG: Email failed to send - {e}")
        messages.error(request, f"Booking was created, but email failed: {e}")




